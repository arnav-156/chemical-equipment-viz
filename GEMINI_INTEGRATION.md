# 🤖 Gemini AI Integration Guide

## Overview

This guide explains how to integrate Google's Gemini AI into the Chemical Equipment Visualizer for enhanced analytics and insights.

## When to Use Gemini

Gemini integration is **optional** and can be added in later phases for:
- AI-powered data insights
- Anomaly detection
- Natural language queries
- Intelligent report summaries
- Equipment recommendations

## Getting Gemini API Key

### Step 1: Get Free API Key

1. Visit: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy your API key (starts with `AIza...`)

**Note**: Gemini API has a generous free tier:
- 60 requests per minute
- 1,500 requests per day
- Perfect for development and testing

### Step 2: Install Gemini SDK

Add to `requirements.txt`:
```
google-generativeai==0.3.1
```

Install:
```bash
pip install google-generativeai
```

### Step 3: Configure API Key

**Option A: Environment Variable (Recommended)**

Create `.env` file in project root:
```env
GEMINI_API_KEY=your_api_key_here
```

Update `backend/settings.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
```

**Option B: Django Settings**
```python
# backend/settings.py
GEMINI_API_KEY = 'your_api_key_here'  # Not recommended for production
```

## Implementation Examples

### Example 1: AI-Powered Data Insights

Create `equipment/ai_insights.py`:

```python
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_equipment_insights(dataset):
    """Generate AI insights for equipment data"""
    summary = dataset.get_summary()
    equipment_items = dataset.equipment_items.all()
    
    # Prepare data for AI
    data_summary = f"""
    Analyze this chemical equipment data:
    
    Total Equipment: {summary['total_count']}
    Average Flowrate: {summary['avg_flowrate']:.2f}
    Average Pressure: {summary['avg_pressure']:.2f}
    Average Temperature: {summary['avg_temperature']:.2f}
    
    Equipment Types: {summary['type_distribution']}
    
    Provide:
    1. Key observations
    2. Potential issues or anomalies
    3. Optimization recommendations
    """
    
    response = model.generate_content(data_summary)
    return response.text

def detect_anomalies(equipment_data):
    """Detect anomalies in equipment parameters"""
    prompt = f"""
    Analyze these equipment parameters and identify any anomalies:
    
    Equipment: {equipment_data['name']}
    Type: {equipment_data['type']}
    Flowrate: {equipment_data['flowrate']}
    Pressure: {equipment_data['pressure']}
    Temperature: {equipment_data['temperature']}
    
    Are these values normal for this equipment type?
    Flag any concerns.
    """
    
    response = model.generate_content(prompt)
    return response.text
```

### Example 2: Add AI Insights Endpoint

Update `equipment/views.py`:

```python
from .ai_insights import generate_equipment_insights

class DatasetViewSet(viewsets.ModelViewSet):
    # ... existing code ...
    
    @action(detail=True, methods=['get'])
    def ai_insights(self, request, pk=None):
        """Get AI-generated insights for dataset"""
        dataset = self.get_object()
        
        try:
            insights = generate_equipment_insights(dataset)
            return Response({
                'insights': insights,
                'generated_at': timezone.now()
            })
        except Exception as e:
            return Response(
                {'error': f'AI insights generation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
```

Add URL:
```python
# New endpoint: GET /api/datasets/<id>/ai_insights/
```

### Example 3: Natural Language Queries

```python
def natural_language_query(query_text, dataset):
    """Process natural language queries about equipment data"""
    equipment_items = dataset.equipment_items.all()
    
    # Convert equipment data to text
    equipment_text = "\n".join([
        f"{item.name}: Type={item.type}, Flowrate={item.flowrate}, "
        f"Pressure={item.pressure}, Temperature={item.temperature}"
        for item in equipment_items
    ])
    
    prompt = f"""
    Equipment Data:
    {equipment_text}
    
    User Question: {query_text}
    
    Provide a clear, concise answer based on the data above.
    """
    
    response = model.generate_content(prompt)
    return response.text
```

### Example 4: Enhanced PDF Reports with AI Summary

Update `equipment/views.py`:

```python
@action(detail=True, methods=['get'])
def report(self, request, pk=None):
    """Generate PDF report with AI insights"""
    dataset = self.get_object()
    
    # Generate AI insights
    try:
        ai_insights = generate_equipment_insights(dataset)
    except:
        ai_insights = "AI insights unavailable"
    
    # Add AI insights section to PDF
    elements.append(Paragraph("<b>AI-Generated Insights</b>", styles['Heading2']))
    elements.append(Paragraph(ai_insights, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # ... rest of PDF generation ...
```

## Frontend Integration

### React Web Frontend

```javascript
// src/services/api.js
export const getAIInsights = async (datasetId, token) => {
  const response = await axios.get(
    `${API_BASE_URL}/datasets/${datasetId}/ai_insights/`,
    {
      headers: { Authorization: `Token ${token}` }
    }
  );
  return response.data;
};

// src/components/AIInsights.jsx
import React, { useState, useEffect } from 'react';
import { getAIInsights } from '../services/api';

function AIInsights({ datasetId }) {
  const [insights, setInsights] = useState('');
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchInsights = async () => {
      try {
        const data = await getAIInsights(datasetId, token);
        setInsights(data.insights);
      } catch (error) {
        console.error('Failed to load AI insights:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchInsights();
  }, [datasetId]);
  
  if (loading) return <div>Generating AI insights...</div>;
  
  return (
    <div className="ai-insights">
      <h3>🤖 AI-Powered Insights</h3>
      <p>{insights}</p>
    </div>
  );
}
```

### PyQt5 Desktop App

```python
# desktop-app/ai_insights_widget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
import requests

class AIInsightsWidget(QWidget):
    def __init__(self, dataset_id, token):
        super().__init__()
        self.dataset_id = dataset_id
        self.token = token
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.insights_text = QTextEdit()
        self.insights_text.setReadOnly(True)
        
        generate_btn = QPushButton("🤖 Generate AI Insights")
        generate_btn.clicked.connect(self.generate_insights)
        
        layout.addWidget(QLabel("AI-Powered Insights"))
        layout.addWidget(self.insights_text)
        layout.addWidget(generate_btn)
        
        self.setLayout(layout)
    
    def generate_insights(self):
        self.insights_text.setText("Generating insights...")
        
        try:
            response = requests.get(
                f'http://localhost:8000/api/datasets/{self.dataset_id}/ai_insights/',
                headers={'Authorization': f'Token {self.token}'}
            )
            
            if response.status_code == 200:
                insights = response.json()['insights']
                self.insights_text.setText(insights)
            else:
                self.insights_text.setText("Failed to generate insights")
        except Exception as e:
            self.insights_text.setText(f"Error: {str(e)}")
```

## Cost Considerations

### Gemini API Pricing (as of 2024)

**Free Tier:**
- 60 requests per minute
- 1,500 requests per day
- Perfect for development and small projects

**Paid Tier (if needed):**
- Pay-as-you-go pricing
- Very affordable for most use cases
- ~$0.00025 per 1K characters

### Optimization Tips

1. **Cache Results**: Store AI insights in database
2. **Rate Limiting**: Limit AI calls per user
3. **Batch Processing**: Process multiple items together
4. **Fallback**: Have non-AI alternatives

## Security Best Practices

1. **Never commit API keys** to Git
2. **Use environment variables**
3. **Add `.env` to `.gitignore`**
4. **Rotate keys regularly**
5. **Use different keys for dev/prod**

## Testing

```python
# equipment/tests/test_ai_insights.py
from django.test import TestCase
from unittest.mock import patch
from equipment.ai_insights import generate_equipment_insights

class AIInsightsTestCase(TestCase):
    @patch('equipment.ai_insights.model.generate_content')
    def test_generate_insights(self, mock_generate):
        mock_generate.return_value.text = "Test insights"
        
        # Test with mock data
        insights = generate_equipment_insights(dataset)
        
        self.assertIn("Test insights", insights)
```

## Current Status

- ✅ Backend ready for Gemini integration
- ⏳ Gemini integration (optional, can be added anytime)
- ⏳ Frontend AI features (Phase 2+)

## When to Add Gemini

**Recommended Timeline:**
1. **Phase 1**: ✅ Complete (no AI needed)
2. **Phase 2**: Build React frontend (basic features first)
3. **Phase 3**: Build PyQt5 desktop app (basic features first)
4. **Phase 4**: Add Gemini AI features (enhancement)
5. **Phase 5**: Deploy with AI capabilities

**Or add it anytime as an enhancement!**

## Alternative: Use Gemini Later

You can complete the entire project without Gemini and add it as a "bonus feature" later. The core functionality (CSV upload, visualization, reports) works perfectly without AI.

## Resources

- **Gemini API Docs**: https://ai.google.dev/docs
- **Python SDK**: https://github.com/google/generative-ai-python
- **Pricing**: https://ai.google.dev/pricing
- **Examples**: https://ai.google.dev/examples

## Summary

**Do you need Gemini now?** 
- ❌ No, not for Phase 1 (backend complete)
- ❌ No, not for Phase 2 (React frontend basics)
- ❌ No, not for Phase 3 (PyQt5 desktop basics)
- ✅ Yes, if you want AI-powered insights (optional enhancement)

**Recommendation**: Complete the basic project first, then add Gemini as an impressive bonus feature!
