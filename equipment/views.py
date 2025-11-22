from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Dataset, Equipment
from .serializers import DatasetSerializer, DatasetListSerializer, EquipmentSerializer
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch


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
                'type_distribution': df['Type'].value_counts().to_dict()
            }
            
            dataset.set_summary(summary)
            dataset.save()
            
            # Cleanup old datasets (keep last 5)
            old_datasets = Dataset.objects.all()[5:]
            for old_dataset in old_datasets:
                old_dataset.delete()
            
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get analytics summary for a dataset"""
        dataset = self.get_object()
        return Response(dataset.get_summary())
    
    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """Generate PDF report for a dataset"""
        dataset = self.get_object()
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
        
        # Summary section
        summary_text = f"""
        <b>Summary Statistics</b><br/>
        Total Equipment: {summary.get('total_count', 0)}<br/>
        Average Flowrate: {summary.get('avg_flowrate', 0):.2f}<br/>
        Average Pressure: {summary.get('avg_pressure', 0):.2f}<br/>
        Average Temperature: {summary.get('avg_temperature', 0):.2f}<br/>
        """
        elements.append(Paragraph(summary_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Equipment table
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
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
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
