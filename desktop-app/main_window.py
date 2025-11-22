"""
Main Window for Chemical Equipment Visualizer Desktop App
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                             QFileDialog, QMessageBox, QTabWidget, QTextEdit,
                             QSplitter, QGroupBox, QGridLayout, QHeaderView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import os
import sys


class UploadThread(QThread):
    """Thread for uploading CSV files"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
    
    def run(self):
        try:
            result = self.api_client.upload_csv(self.file_path)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self, api_client, user_data):
        super().__init__()
        self.api_client = api_client
        self.user_data = user_data
        self.current_dataset = None
        self.current_summary = None
        self.init_ui()
        self.load_datasets()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setGeometry(100, 100, 1400, 900)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_upload_tab(), '📤 Upload')
        self.tabs.addTab(self.create_datasets_tab(), '📊 Datasets')
        self.tabs.addTab(self.create_analytics_tab(), '📈 Analytics')
        self.tabs.addTab(self.create_charts_tab(), '📉 Charts')
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage('Ready')
        
        central_widget.setLayout(main_layout)
        
        # Apply stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background: white;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 3px solid #667eea;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        upload_action = file_menu.addAction('Upload CSV')
        upload_action.triggered.connect(self.upload_csv)
        
        download_action = file_menu.addAction('Download Report')
        download_action.triggered.connect(self.download_report)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        refresh_action = view_menu.addAction('Refresh Datasets')
        refresh_action.triggered.connect(self.load_datasets)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = help_menu.addAction('About')
        about_action.triggered.connect(self.show_about)
    
    def create_header(self):
        """Create header widget"""
        header = QWidget()
        header.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #764ba2); padding: 15px;')
        layout = QHBoxLayout()
        
        title = QLabel('🧪 Chemical Equipment Visualizer')
        title.setStyleSheet('color: white; font-size: 20px; font-weight: bold;')
        layout.addWidget(title)
        
        layout.addStretch()
        
        user_label = QLabel(f"Welcome, {self.user_data.get('username', 'User')}!")
        user_label.setStyleSheet('color: white; font-size: 14px;')
        layout.addWidget(user_label)
        
        logout_btn = QPushButton('Logout')
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        header.setLayout(layout)
        return header
    
    def create_upload_tab(self):
        """Create upload tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Upload section
        upload_group = QGroupBox('Upload CSV File')
        upload_layout = QVBoxLayout()
        
        info_label = QLabel('Select a CSV file with equipment data to upload and analyze.')
        info_label.setWordWrap(True)
        upload_layout.addWidget(info_label)
        
        format_label = QLabel('<b>Required format:</b> Equipment Name, Type, Flowrate, Pressure, Temperature')
        format_label.setStyleSheet('color: #666; margin: 10px 0;')
        upload_layout.addWidget(format_label)
        
        btn_layout = QHBoxLayout()
        
        select_btn = QPushButton('📁 Select CSV File')
        select_btn.setStyleSheet('background-color: #667eea; color: white;')
        select_btn.clicked.connect(self.upload_csv)
        btn_layout.addWidget(select_btn)
        
        btn_layout.addStretch()
        
        upload_layout.addLayout(btn_layout)
        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)
        
        # Recent uploads
        recent_group = QGroupBox('Recent Uploads')
        recent_layout = QVBoxLayout()
        
        self.upload_status = QTextEdit()
        self.upload_status.setReadOnly(True)
        self.upload_status.setMaximumHeight(200)
        self.upload_status.setPlaceholderText('Upload history will appear here...')
        recent_layout.addWidget(self.upload_status)
        
        recent_group.setLayout(recent_layout)
        layout.addWidget(recent_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_datasets_tab(self):
        """Create datasets tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        refresh_btn = QPushButton('🔄 Refresh')
        refresh_btn.clicked.connect(self.load_datasets)
        toolbar.addWidget(refresh_btn)
        
        toolbar.addStretch()
        
        view_btn = QPushButton('👁️ View Details')
        view_btn.clicked.connect(self.view_dataset_details)
        toolbar.addWidget(view_btn)
        
        layout.addLayout(toolbar)
        
        # Dataset table
        self.dataset_table = QTableWidget()
        self.dataset_table.setColumnCount(4)
        self.dataset_table.setHorizontalHeaderLabels(['ID', 'File Name', 'Upload Date', 'Equipment Count'])
        self.dataset_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.dataset_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.dataset_table.setSelectionMode(QTableWidget.SingleSelection)
        self.dataset_table.doubleClicked.connect(self.view_dataset_details)
        layout.addWidget(self.dataset_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_analytics_tab(self):
        """Create analytics tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summary cards
        cards_layout = QGridLayout()
        
        self.total_card = self.create_stat_card('Total Equipment', '0', '#667eea')
        self.flowrate_card = self.create_stat_card('Avg Flowrate', '0.00', '#4caf50')
        self.pressure_card = self.create_stat_card('Avg Pressure', '0.00', '#ff9800')
        self.temp_card = self.create_stat_card('Avg Temperature', '0.00', '#f44336')
        
        cards_layout.addWidget(self.total_card, 0, 0)
        cards_layout.addWidget(self.flowrate_card, 0, 1)
        cards_layout.addWidget(self.pressure_card, 1, 0)
        cards_layout.addWidget(self.temp_card, 1, 1)
        
        layout.addLayout(cards_layout)
        
        # Equipment table
        equipment_group = QGroupBox('Equipment Details')
        equipment_layout = QVBoxLayout()
        
        self.equipment_table = QTableWidget()
        self.equipment_table.setColumnCount(5)
        self.equipment_table.setHorizontalHeaderLabels(['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.equipment_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        equipment_layout.addWidget(self.equipment_table)
        
        equipment_group.setLayout(equipment_layout)
        layout.addWidget(equipment_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_charts_tab(self):
        """Create charts tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        download_report_btn = QPushButton('📄 Download PDF Report')
        download_report_btn.setStyleSheet('background-color: #4caf50; color: white;')
        download_report_btn.clicked.connect(self.download_report)
        toolbar.addWidget(download_report_btn)
        
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # Charts
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        widget.setLayout(layout)
        return widget
    
    def create_stat_card(self, title, value, color):
        """Create a statistics card"""
        card = QGroupBox()
        card.setStyleSheet(f'border-top: 4px solid {color};')
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet('font-size: 12px; color: #666;')
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #333;')
        value_label.setObjectName('value_label')
        layout.addWidget(value_label)
        
        card.setLayout(layout)
        return card
    
    def upload_csv(self):
        """Handle CSV upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Select CSV File',
            '',
            'CSV Files (*.csv);;All Files (*)'
        )
        
        if not file_path:
            return
        
        self.statusBar().showMessage('Uploading file...')
        self.upload_status.append(f'Uploading: {os.path.basename(file_path)}...')
        
        # Create and start upload thread
        self.upload_thread = UploadThread(self.api_client, file_path)
        self.upload_thread.finished.connect(self.on_upload_success)
        self.upload_thread.error.connect(self.on_upload_error)
        self.upload_thread.start()
    
    def on_upload_success(self, data):
        """Handle successful upload"""
        self.statusBar().showMessage('Upload successful!')
        self.upload_status.append(f'✅ Successfully uploaded: {data.get("file_name")}')
        self.upload_status.append(f'   Equipment count: {data.get("summary", {}).get("total_count", 0)}')
        self.upload_status.append('')
        
        QMessageBox.information(self, 'Success', 'File uploaded successfully!')
        self.load_datasets()
        self.load_dataset_details(data['id'])
    
    def on_upload_error(self, error):
        """Handle upload error"""
        self.statusBar().showMessage('Upload failed')
        self.upload_status.append(f'❌ Upload failed: {error}')
        self.upload_status.append('')
        QMessageBox.critical(self, 'Upload Failed', f'Failed to upload file:\n{error}')
    
    def load_datasets(self):
        """Load datasets from API"""
        try:
            datasets = self.api_client.get_datasets()
            self.populate_dataset_table(datasets)
            self.statusBar().showMessage(f'Loaded {len(datasets)} datasets')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load datasets:\n{str(e)}')
    
    def populate_dataset_table(self, datasets):
        """Populate dataset table"""
        self.dataset_table.setRowCount(len(datasets))
        
        for row, dataset in enumerate(datasets):
            self.dataset_table.setItem(row, 0, QTableWidgetItem(str(dataset['id'])))
            self.dataset_table.setItem(row, 1, QTableWidgetItem(dataset['file_name']))
            self.dataset_table.setItem(row, 2, QTableWidgetItem(dataset['upload_date']))
            self.dataset_table.setItem(row, 3, QTableWidgetItem(str(dataset['equipment_count'])))
    
    def view_dataset_details(self):
        """View selected dataset details"""
        selected_rows = self.dataset_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'No Selection', 'Please select a dataset to view')
            return
        
        dataset_id = int(self.dataset_table.item(selected_rows[0].row(), 0).text())
        self.load_dataset_details(dataset_id)
    
    def load_dataset_details(self, dataset_id):
        """Load dataset details"""
        try:
            self.current_dataset = self.api_client.get_dataset(dataset_id)
            self.current_summary = self.api_client.get_summary(dataset_id)
            
            self.update_analytics()
            self.update_charts()
            self.tabs.setCurrentIndex(2)  # Switch to analytics tab
            
            self.statusBar().showMessage(f'Loaded dataset: {self.current_dataset["file_name"]}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load dataset:\n{str(e)}')
    
    def update_analytics(self):
        """Update analytics tab with current dataset"""
        if not self.current_summary:
            return
        
        # Update stat cards
        self.total_card.findChild(QLabel, 'value_label').setText(str(self.current_summary['total_count']))
        self.flowrate_card.findChild(QLabel, 'value_label').setText(f"{self.current_summary['avg_flowrate']:.2f}")
        self.pressure_card.findChild(QLabel, 'value_label').setText(f"{self.current_summary['avg_pressure']:.2f}")
        self.temp_card.findChild(QLabel, 'value_label').setText(f"{self.current_summary['avg_temperature']:.2f}")
        
        # Update equipment table
        equipment_items = self.current_dataset.get('equipment_items', [])
        self.equipment_table.setRowCount(len(equipment_items))
        
        for row, item in enumerate(equipment_items):
            self.equipment_table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.equipment_table.setItem(row, 1, QTableWidgetItem(item['type']))
            self.equipment_table.setItem(row, 2, QTableWidgetItem(f"{item['flowrate']:.2f}"))
            self.equipment_table.setItem(row, 3, QTableWidgetItem(f"{item['pressure']:.2f}"))
            self.equipment_table.setItem(row, 4, QTableWidgetItem(f"{item['temperature']:.2f}"))
    
    def update_charts(self):
        """Update charts with current dataset"""
        if not self.current_summary or not self.current_dataset:
            return
        
        self.figure.clear()
        
        # Create subplots
        ax1 = self.figure.add_subplot(2, 2, 1)
        ax2 = self.figure.add_subplot(2, 2, 2)
        ax3 = self.figure.add_subplot(2, 2, 3)
        ax4 = self.figure.add_subplot(2, 2, 4)
        
        # Chart 1: Equipment Type Distribution (Bar)
        type_dist = self.current_summary.get('type_distribution', {})
        if type_dist:
            ax1.bar(type_dist.keys(), type_dist.values(), color='steelblue')
            ax1.set_xlabel('Equipment Type')
            ax1.set_ylabel('Count')
            ax1.set_title('Equipment Type Distribution')
            ax1.tick_params(axis='x', rotation=45)
        
        # Chart 2: Parameter Trends (Line)
        equipment_items = self.current_dataset.get('equipment_items', [])
        if equipment_items:
            names = [item['name'][:10] for item in equipment_items]  # Truncate names
            flowrates = [item['flowrate'] for item in equipment_items]
            pressures = [item['pressure'] for item in equipment_items]
            temperatures = [item['temperature'] for item in equipment_items]
            
            x = range(len(names))
            ax2.plot(x, flowrates, 'o-', label='Flowrate', color='#4caf50')
            ax2.plot(x, pressures, 's-', label='Pressure', color='#ff9800')
            ax2.plot(x, temperatures, '^-', label='Temperature', color='#f44336')
            ax2.set_xlabel('Equipment')
            ax2.set_ylabel('Value')
            ax2.set_title('Parameter Trends')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        # Chart 3: Type Distribution (Pie)
        if type_dist:
            ax3.pie(type_dist.values(), labels=type_dist.keys(), autopct='%1.1f%%', startangle=90)
            ax3.set_title('Type Distribution')
        
        # Chart 4: Parameter Ranges
        if self.current_summary:
            params = ['Flowrate', 'Pressure', 'Temperature']
            avgs = [
                self.current_summary['avg_flowrate'],
                self.current_summary['avg_pressure'],
                self.current_summary['avg_temperature']
            ]
            mins = [
                self.current_summary['min_flowrate'],
                self.current_summary['min_pressure'],
                self.current_summary['min_temperature']
            ]
            maxs = [
                self.current_summary['max_flowrate'],
                self.current_summary['max_pressure'],
                self.current_summary['max_temperature']
            ]
            
            x = range(len(params))
            ax4.bar(x, avgs, color='steelblue', label='Average')
            ax4.errorbar(x, avgs, yerr=[
                [avgs[i] - mins[i] for i in range(len(avgs))],
                [maxs[i] - avgs[i] for i in range(len(avgs))]
            ], fmt='none', color='red', capsize=5, label='Min/Max Range')
            ax4.set_xticks(x)
            ax4.set_xticklabels(params)
            ax4.set_ylabel('Value')
            ax4.set_title('Parameter Ranges')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def download_report(self):
        """Download PDF report"""
        if not self.current_dataset:
            QMessageBox.warning(self, 'No Dataset', 'Please select a dataset first')
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            'Save PDF Report',
            f"{self.current_dataset['file_name']}_report.pdf",
            'PDF Files (*.pdf)'
        )
        
        if not file_path:
            return
        
        try:
            self.api_client.download_report(self.current_dataset['id'], file_path)
            QMessageBox.information(self, 'Success', f'Report saved to:\n{file_path}')
            
            # Ask to open
            reply = QMessageBox.question(
                self, 'Open Report',
                'Do you want to open the report?',
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                os.startfile(file_path) if sys.platform == 'win32' else os.system(f'open "{file_path}"')
        
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to download report:\n{str(e)}')
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            'About Chemical Equipment Visualizer',
            '<h2>Chemical Equipment Visualizer</h2>'
            '<p>Version 1.0</p>'
            '<p>A desktop application for analyzing and visualizing chemical equipment data.</p>'
            '<p><b>Features:</b></p>'
            '<ul>'
            '<li>CSV file upload and analysis</li>'
            '<li>Interactive data visualization</li>'
            '<li>PDF report generation</li>'
            '<li>Real-time analytics</li>'
            '</ul>'
            '<p>Built with PyQt5, Matplotlib, and Django REST API</p>'
        )
    
    def logout(self):
        """Logout user"""
        reply = QMessageBox.question(
            self, 'Logout',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.api_client.logout()
            self.close()
