import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="SANKET Monitor", layout="wide", initial_sidebar_state="collapsed") 

def load_processed_data():
    # Load the stressful data generated in Phase 2 [cite: 42]
    df = pd.read_csv('data/stress_test_logs.csv')
    
    # DATA NORMALIZATION: Convert to uppercase and strip whitespace to prevent KeyErrors
    df['transaction_type'] = df['transaction_type'].str.upper().str.strip()
    
    # Calculate health metrics: amount < 0 or status 500 is an error [cite: 45]
    df['is_error'] = (df['amount'] < 0) | (df['status_code'] == 500)
    # Slow if latency > 500ms and not an error [cite: 47]
    df['is_slow'] = (df['latency_ms'] > 500) & (~df['is_error'])
    
    # Group by service type to aggregate failures [cite: 50, 54]
    summary = df.groupby('transaction_type').agg(
        total=('transaction_id', 'count'),
        errors=('is_error', 'sum'),
        slow=('is_slow', 'sum')
    ).reset_index() 
    
    # Calculate a Health Score (0 to 100) [cite: 56]
    summary['health_score'] = 100 - ((summary['errors'] / summary['total']) * 100) 
    
    # Define Satellite Topology (Coordinates for the map)
    topology = {
        'CREDIT': [1, 4], 'DEBT': [2, 1], 
        'PAYMENT': [4, 3], 'TRANSFER': [6, 2]
    }
    
    # Use .get() to safely map coordinates; defaults to [0,0] if a service is missing
    summary['x'] = summary['transaction_type'].apply(lambda x: topology.get(x, [0, 0])[0])
    summary['y'] = summary['transaction_type'].apply(lambda x: topology.get(x, [0, 0])[1])
    
    return summary

# UI Header
st.title("SANKET | Systemic Analysis of Network-Knot Error Tracking") 
data = load_processed_data()

# Visual Topography (The Map) 
fig = go.Figure()

# Draw "Highways" (Connections)
connections = [('CREDIT', 'PAYMENT'), ('DEBT', 'PAYMENT'), ('PAYMENT', 'TRANSFER')]
for start, end in connections:
    # Safely extract rows for the start and end nodes
    s_row = data[data['transaction_type'] == start]
    e_row = data[data['transaction_type'] == end]
    
    # Only draw the line if both services exist in the current data
    if not s_row.empty and not e_row.empty:
        fig.add_trace(go.Scatter(
            x=[s_row['x'].values[0], e_row['x'].values[0]],
            y=[s_row['y'].values[0], e_row['y'].values[0]],
            mode='lines', 
            line=dict(color='#444', width=1), 
            hoverinfo='none'
        ))

# Draw "Service Nodes" (The Satellites)

fig.add_trace(go.Scatter(
    x=data['x'], y=data['y'], 
    mode='markers+text',
    text=data['transaction_type'], 
    textposition="top center",
    marker=dict(
        size=45, 
        color=data['health_score'], 
        colorscale='RdYlGn', 
        showscale=True,
        line=dict(width=2, color='white')
    )
))

fig.update_layout(
    height=500, 
    showlegend=False, 
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True) 

# Metrics Grid 
cols = st.columns(len(data))
for i, row in data.iterrows():
    with cols[i]:
        st.metric(row['transaction_type'], f"{row['health_score']:.1f}%") 
        st.caption(f"Failures: {int(row['errors'])} | Latency: {int(row['slow'])}")