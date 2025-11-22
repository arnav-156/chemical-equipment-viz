from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.cache import cache
from .models import Dataset, Equipment, AlertRule, AlertHistory
from .serializers import DatasetSerializer, DatasetListSerializer, EquipmentSerializer, AlertRuleSerializer, AlertHistorySerializer
from .alerts import AlertManager, check_anomalies
from .anomaly_detection import AnomalyDetector, get_dataset_health_summary
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DatasetListSerializer
        return DatasetSerializer
    
    def list(self, request):
        """Get last 5 datasets"""
        datasets = Dataset.objects.all()[:5]
        serializer = self.get_serializer(datasets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Handle CSV file upload"""
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        csv_file = request.FILES['file']
        
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Read CSV file
            df = pd.read_csv(csv_file)
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create dataset
            dataset = Dataset.objects.create(
                file_name=csv_file.name,
                uploaded_by=request.user
            )
            
            # Create equipment records
            equipment_list = []
            for _, row in df.iterrows():
                equipment = Equipment(
                    dataset=dataset,
                    name=row['Equipment Name'],
                    type=row['Type'],
                    flowrate=float(row['Flowrate']),
                    pressure=float(row['Pressure']),
                    temperature=float(row['Temperature'])
                )
                equipment_list.append(equipment)
            
            Equipment.objects.bulk_create(equipment_list)
            
            # Calculate summary statistics
            summary = {
                'total_count': len(df),
                'avg_flowrate': float(df['Flowrate'].mean()),
                'avg_pressure': float(df['Pressure'].mean()),
                'avg_temperature': float(df['Temperature'].mean()),
                'min_flowrate': float(df['Flowrate'].min()),
                'max_flowrate': float(df['Flowrate'].max()),
                'min_pressure': float(df['Pressure'].min()),
                'max_pressure': float(df['Pressure'].max()),
                'min_temperature': float(df['Temperature'].min()),
                'max_temperature': float(df['Temperature'].max()),
                'type_distribution': df['Type'].value_counts().to_dict()
            }
            
            dataset.set_summary(summary)
            dataset.save()
            
            # Check for alerts
            alert_manager = AlertManager()
            alerts = alert_manager.check_dataset(dataset)
            
            # Cleanup old datasets (keep last 5)
            old_datasets = Dataset.objects.all()[5:]
            for old_dataset in old_datasets:
                old_dataset.delete()
            
            serializer = DatasetSerializer(dataset)
            response_data = serializer.data
            response_data['alerts_triggered'] = len(alerts)
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get analytics summary for a dataset"""
        dataset = self.get_object()
        return Response(dataset.get_summary())
    
    @action(detail=True, methods=['get'])
    def anomalies(self, request, pk=None):
        """Detect anomalies in dataset using ML"""
        dataset = self.get_object()
        equipment_items = list(dataset.equipment_items.all())
        
        if not equipment_items:
            return Response({'error': 'No equipment data found'}, status=status.HTTP_404_NOT_FOUND)
        
        detector = AnomalyDetector()
        anomalies = detector.detect_anomalies(equipment_items)
        
        return Response({
            'dataset_id': dataset.id,
            'dataset_name': dataset.file_name,
            'total_equipment': len(equipment_items),
            'anomalies': anomalies,
            'health_summary': get_dataset_health_summary(dataset)
        })
    
    @action(detail=True, methods=['get'])
    def health(self, request, pk=None):
        """Get health summary for dataset"""
        dataset = self.get_object()
        health_summary = get_dataset_health_summary(dataset)
        return Response(health_summary)
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """Analyze trends across recent datasets"""
        datasets = Dataset.objects.all()[:3]
        
        if len(datasets) < 2:
            return Response({
                'message': 'Need at least 2 datasets for trend analysis',
                'trends': None
            })
        
        detector = AnomalyDetector()
        trends = detector.analyze_trends(datasets)
        
        return Response({
            'datasets_analyzed': len(datasets),
            'trends': trends
        })
    
    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """Generate PDF report for a dataset with charts and caching"""
        dataset = self.get_object()
        
        # Check cache first
        cache_key = f'pdf_report_{dataset.id}_{dataset.upload_date.timestamp()}'
        cached_pdf = cache.get(cache_key)
        
        if cached_pdf:
            response = HttpResponse(cached_pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{dataset.file_name}_report.pdf"'
            return response
        
        equipment_items = dataset.equipment_items.all()
        summary = dataset.get_summary()
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"<b>Equipment Report: {dataset.file_name}</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary section with min/max
        summary_text = f"""
        <b>Summary Statistics</b><br/>
        Total Equipment: {summary.get('total_count', 0)}<br/>
        <br/>
        <b>Flowrate:</b> Avg: {summary.get('avg_flowrate', 0):.2f}, 
        Min: {summary.get('min_flowrate', 0):.2f}, 
        Max: {summary.get('max_flowrate', 0):.2f}<br/>
        <b>Pressure:</b> Avg: {summary.get('avg_pressure', 0):.2f}, 
        Min: {summary.get('min_pressure', 0):.2f}, 
        Max: {summary.get('max_pressure', 0):.2f}<br/>
        <b>Temperature:</b> Avg: {summary.get('avg_temperature', 0):.2f}, 
        Min: {summary.get('min_temperature', 0):.2f}, 
        Max: {summary.get('max_temperature', 0):.2f}<br/>
        """
        elements.append(Paragraph(summary_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Generate charts
        try:
            # Chart 1: Equipment Type Distribution
            type_dist = summary.get('type_distribution', {})
            if type_dist:
                fig, ax = plt.subplots(figsize=(6, 4))
                types = list(type_dist.keys())
                counts = list(type_dist.values())
                ax.bar(types, counts, color='steelblue')
                ax.set_xlabel('Equipment Type')
                ax.set_ylabel('Count')
                ax.set_title('Equipment Type Distribution')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                # Save chart to buffer
                chart_buffer = io.BytesIO()
                plt.savefig(chart_buffer, format='png', dpi=150, bbox_inches='tight')
                chart_buffer.seek(0)
                plt.close()
                
                # Add chart to PDF
                chart_image = Image(chart_buffer, width=5*inch, height=3.5*inch)
                elements.append(Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2']))
                elements.append(Spacer(1, 0.1*inch))
                elements.append(chart_image)
                elements.append(Spacer(1, 0.3*inch))
            
            # Chart 2: Parameter Comparison
            fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 3))
            
            # Flowrate
            flowrates = [item.flowrate for item in equipment_items]
            ax1.hist(flowrates, bins=10, color='skyblue', edgecolor='black')
            ax1.set_xlabel('Flowrate')
            ax1.set_ylabel('Frequency')
            ax1.set_title('Flowrate Distribution')
            
            # Pressure
            pressures = [item.pressure for item in equipment_items]
            ax2.hist(pressures, bins=10, color='lightcoral', edgecolor='black')
            ax2.set_xlabel('Pressure')
            ax2.set_ylabel('Frequency')
            ax2.set_title('Pressure Distribution')
            
            # Temperature
            temperatures = [item.temperature for item in equipment_items]
            ax3.hist(temperatures, bins=10, color='lightgreen', edgecolor='black')
            ax3.set_xlabel('Temperature')
            ax3.set_ylabel('Frequency')
            ax3.set_title('Temperature Distribution')
            
            plt.tight_layout()
            
            # Save chart to buffer
            chart_buffer2 = io.BytesIO()
            plt.savefig(chart_buffer2, format='png', dpi=150, bbox_inches='tight')
            chart_buffer2.seek(0)
            plt.close()
            
            # Add chart to PDF
            chart_image2 = Image(chart_buffer2, width=7*inch, height=2.5*inch)
            elements.append(Paragraph("<b>Parameter Distributions</b>", styles['Heading2']))
            elements.append(Spacer(1, 0.1*inch))
            elements.append(chart_image2)
            elements.append(Spacer(1, 0.3*inch))
            
        except Exception as e:
            # If chart generation fails, continue without charts
            elements.append(Paragraph(f"<i>Chart generation skipped: {str(e)}</i>", styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Equipment table
        elements.append(Paragraph("<b>Equipment Details</b>", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
        for item in equipment_items:
            data.append([
                item.name,
                item.type,
                f"{item.flowrate:.2f}",
                f"{item.pressure:.2f}",
                f"{item.temperature:.2f}"
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        buffer.seek(0)
        pdf_content = buffer.read()
        
        # Cache the PDF for 1 hour
        cache.set(cache_key, pdf_content, 3600)
        
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{dataset.file_name}_report.pdf"'
        return response


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Handle user login"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Handle user logout"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'})
    except:
        return Response({'error': 'Logout failed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Handle user registration"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password, email=email)
    token = Token.objects.create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    }, status=status.HTTP_201_CREATED)



class AlertRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing alert rules"""
    queryset = AlertRule.objects.all()
    serializer_class = AlertRuleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter active rules"""
        queryset = AlertRule.objects.all()
        active_only = self.request.query_params.get('active', None)
        if active_only == 'true':
            queryset = queryset.filter(is_active=True)
        return queryset


class AlertHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing alert history"""
    queryset = AlertHistory.objects.all()
    serializer_class = AlertHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter alerts"""
        queryset = AlertHistory.objects.all()
        
        # Filter by severity
        severity = self.request.query_params.get('severity', None)
        if severity:
            queryset = queryset.filter(severity=severity)
        
        # Filter by acknowledged status
        acknowledged = self.request.query_params.get('acknowledged', None)
        if acknowledged == 'false':
            queryset = queryset.filter(acknowledged=False)
        
        # Limit to recent alerts
        limit = self.request.query_params.get('limit', 50)
        queryset = queryset[:int(limit)]
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge an alert"""
        alert = self.get_object()
        alert.acknowledged = True
        alert.acknowledged_at = timezone.now()
        alert.save()
        
        serializer = self.get_serializer(alert)
        return Response(serializer.data)


from django.utils import timezone
