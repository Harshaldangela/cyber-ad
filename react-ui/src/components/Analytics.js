import React from 'react';
import styled from 'styled-components';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import { FaChartBar, FaChartPie } from 'react-icons/fa';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 25px;
`;

const Section = styled.div`
  background: ${props => props.theme.cardBackground};
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 25px;
  border: 1px solid ${props => props.theme.border};
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
  }
`;

const SectionHeader = styled.h2`
  margin-top: 0;
  color: ${props => props.theme.text};
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.4rem;
  font-weight: 600;
  padding-bottom: 15px;
  border-bottom: 2px solid ${props => props.theme.border};
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 25px;
  margin-bottom: 35px;
`;

const StatCard = styled.div`
  background: ${props => props.theme.cardBackground};
  border-radius: 12px;
  padding: 25px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border: 1px solid ${props => props.theme.border};
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
  }
  
  h3 {
    margin: 0 0 15px 0;
    font-size: 2.5rem;
    color: ${props => props.color};
  }
  
  p {
    margin: 0;
    color: ${props => props.theme.text};
    font-weight: 500;
    font-size: 1.1rem;
  }
`;

const ChartContainer = styled.div`
  height: 400px;
  margin-top: 25px;
  background: ${props => props.theme.cardBackground};
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
`;

const Analytics = ({ history, stats }) => {
  // Process data for charts
  const processData = () => {
    // Group by date for trend analysis
    const dailyData = {};
    
    history.forEach(item => {
      const date = new Date(item.timestamp).toISOString().split('T')[0];
      if (!dailyData[date]) {
        dailyData[date] = { spam: 0, notSpam: 0 };
      }
      if (item.result === 'Spam') {
        dailyData[date].spam += 1;
      } else {
        dailyData[date].notSpam += 1;
      }
    });
    
    // Sort dates
    const sortedDates = Object.keys(dailyData).sort();
    
    // Prepare data for bar chart
    const barChartData = {
      labels: sortedDates,
      datasets: [
        {
          label: 'Spam',
          data: sortedDates.map(date => dailyData[date].spam),
          backgroundColor: 'rgba(244, 67, 54, 0.7)',
          borderColor: 'rgba(244, 67, 54, 1)',
          borderWidth: 2,
          borderRadius: 6,
        },
        {
          label: 'Not Spam',
          data: sortedDates.map(date => dailyData[date].notSpam),
          backgroundColor: 'rgba(76, 175, 80, 0.7)',
          borderColor: 'rgba(76, 175, 80, 1)',
          borderWidth: 2,
          borderRadius: 6,
        },
      ],
    };
    
    // Prepare data for pie chart
    const pieChartData = {
      labels: ['Spam', 'Not Spam'],
      datasets: [
        {
          data: [stats.spam, stats.notSpam],
          backgroundColor: [
            'rgba(244, 67, 54, 0.8)',
            'rgba(76, 175, 80, 0.8)',
          ],
          borderColor: [
            'rgba(244, 67, 54, 1)',
            'rgba(76, 175, 80, 1)',
          ],
          borderWidth: 2,
          borderRadius: 6,
        },
      ],
    };
    
    return { barChartData, pieChartData };
  };
  
  const { barChartData, pieChartData } = processData();
  
  const barChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#666',
          font: {
            size: 14
          }
        }
      },
      title: {
        display: true,
        text: 'Classification Trend Over Time',
        color: '#333',
        font: {
          size: 18,
          weight: 'bold'
        }
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          color: '#666',
          font: {
            size: 12
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
      },
      x: {
        ticks: {
          color: '#666',
          font: {
            size: 12
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
      },
    },
  };
  
  const pieChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#666',
          font: {
            size: 14
          }
        }
      },
      title: {
        display: true,
        text: 'Spam vs Not Spam Distribution',
        color: '#333',
        font: {
          size: 18,
          weight: 'bold'
        }
      },
    },
  };
  
  if (history.length === 0) {
    return (
      <Container>
        <Section>
          <SectionHeader>
            <FaChartBar />
            <span>Analytics Dashboard</span>
          </SectionHeader>
          <p>No classification history yet. Analyze some messages to see analytics.</p>
        </Section>
      </Container>
    );
  }
  
  return (
    <Container>
      <Section>
        <SectionHeader>
          <FaChartBar />
          <span>Analytics Dashboard</span>
        </SectionHeader>
        
        <StatsGrid>
          <StatCard color="#1976d2">
            <h3>{history.length}</h3>
            <p>Total Messages</p>
          </StatCard>
          <StatCard color="#f44336">
            <h3>{stats.spam}</h3>
            <p>Spam Detected</p>
          </StatCard>
          <StatCard color="#4caf50">
            <h3>{stats.notSpam}</h3>
            <p>Legitimate</p>
          </StatCard>
        </StatsGrid>
        
        <ChartContainer>
          <Bar data={barChartData} options={barChartOptions} />
        </ChartContainer>
        
        <ChartContainer>
          <Pie data={pieChartData} options={pieChartOptions} />
        </ChartContainer>
      </Section>
    </Container>
  );
};

export default Analytics;