import React, { useState } from 'react';
import styled from 'styled-components';
import { FaHistory, FaTrash, FaExpand, FaCompress, FaFilter } from 'react-icons/fa';

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

const FilterContainer = styled.div`
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const FilterButton = styled.button`
  background: ${props => props.active ? 
    `linear-gradient(135deg, ${props.theme.primary} 0%, #1565c0 100%)` : 
    props.theme.cardBackground};
  color: ${props => props.active ? 'white' : props.theme.text};
  border: 2px solid ${props => props.active ? props.theme.primary : props.theme.border};
  border-radius: 8px;
  padding: 10px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  
  &:hover {
    background: ${props => props.active ? 
      `linear-gradient(135deg, #1565c0 0%, #0d47a1 100%)` : 
      'rgba(0, 0, 0, 0.05)'};
    transform: translateY(-2px);
  }
  
  @media (max-width: 768px) {
    width: 100%;
    justify-content: center;
  }
`;

const ClearButton = styled.button`
  background: linear-gradient(135deg, ${props => props.theme.danger} 0%, #d32f2f 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  margin-left: auto;
  
  &:hover {
    background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
    transform: translateY(-2px);
  }
  
  @media (max-width: 768px) {
    margin-left: 0;
    width: 100%;
    justify-content: center;
  }
`;

const HistoryItem = styled.div`
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 20px;
  border-left: 5px solid ${props => props.type === 'Spam' ? '#f44336' : '#4caf50'};
  background-color: ${props => props.type === 'Spam' ? 
    (props.theme.name === 'dark' ? 'rgba(244, 67, 54, 0.15)' : 'rgba(244, 67, 54, 0.1)') : 
    (props.theme.name === 'dark' ? 'rgba(76, 175, 80, 0.15)' : 'rgba(76, 175, 80, 0.1)')};
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  }
`;

const MessagePreview = styled.div`
  font-style: italic;
  margin: 15px 0;
  color: ${props => props.theme.text};
  background: ${props => props.theme.name === 'dark' ? 'rgba(0, 0, 0, 0.2)' : 'rgba(0, 0, 0, 0.05)'};
  padding: 15px;
  border-radius: 8px;
`;

const AdContent = styled.div`
  background-color: ${props => props.theme.name === 'dark' ? 'rgba(255, 152, 0, 0.15)' : 'rgba(255, 152, 0, 0.1)'};
  border-left: 5px solid #ff9800;
  padding: 20px;
  border-radius: 8px;
  margin: 20px 0;
  white-space: pre-wrap;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 15px;
  margin-top: 20px;
  flex-wrap: wrap;
`;

const ToggleButton = styled.button`
  background: linear-gradient(135deg, ${props => props.theme.primary} 0%, #1565c0 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  
  &:hover {
    background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
    transform: translateY(-2px);
  }
`;

const History = ({ history }) => {
  const [expandedItems, setExpandedItems] = useState({});
  const [filter, setFilter] = useState('all');

  const toggleExpand = (id) => {
    setExpandedItems(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const clearHistory = () => {
    if (window.confirm('Are you sure you want to clear all history?')) {
      localStorage.removeItem('history');
      window.location.reload();
    }
  };

  const filteredHistory = filter === 'all' 
    ? history 
    : history.filter(item => item.result === filter);

  if (history.length === 0) {
    return (
      <Container>
        <Section>
          <SectionHeader>
            <FaHistory />
            <span>Classification History</span>
          </SectionHeader>
          <p>No classification history yet. Analyze some messages to populate history.</p>
        </Section>
      </Container>
    );
  }

  return (
    <Container>
      <Section>
        <SectionHeader>
          <FaHistory />
          <span>Classification History</span>
        </SectionHeader>
        
        <FilterContainer>
          <FilterButton 
            active={filter === 'all'} 
            onClick={() => setFilter('all')}
          >
            <FaFilter />
            All ({history.length})
          </FilterButton>
          <FilterButton 
            active={filter === 'Spam'} 
            onClick={() => setFilter('Spam')}
          >
            <FaFilter />
            Spam ({history.filter(item => item.result === 'Spam').length})
          </FilterButton>
          <FilterButton 
            active={filter === 'Not Spam'} 
            onClick={() => setFilter('Not Spam')}
          >
            <FaFilter />
            Not Spam ({history.filter(item => item.result === 'Not Spam').length})
          </FilterButton>
          <ClearButton 
            onClick={clearHistory}
          >
            <FaTrash />
            Clear History
          </ClearButton>
        </FilterContainer>
        
        {filteredHistory.map((item) => (
          <HistoryItem 
            key={item.id} 
            type={item.result}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
              <div>
                <strong>{new Date(item.timestamp).toLocaleString()}</strong>
                <div>
                  <span style={{ 
                    color: item.result === 'Spam' ? '#f44336' : '#4caf50',
                    fontWeight: 'bold',
                    fontSize: '1.1rem'
                  }}>
                    {item.result}
                  </span>
                </div>
              </div>
            </div>
            
            <MessagePreview>
              "{item.message.length > 150 ? item.message.substring(0, 150) + '...' : item.message}"
            </MessagePreview>
            
            {item.adContent && (
              <>
                <ButtonGroup>
                  <ToggleButton 
                    onClick={() => toggleExpand(item.id)}
                  >
                    {expandedItems[item.id] ? <><FaCompress /> Collapse Ad</> : <><FaExpand /> View Generated Ad</>}
                  </ToggleButton>
                </ButtonGroup>
                
                {expandedItems[item.id] && (
                  <AdContent>
                    {item.adContent}
                  </AdContent>
                )}
              </>
            )}
          </HistoryItem>
        ))}
      </Section>
    </Container>
  );
};

export default History;