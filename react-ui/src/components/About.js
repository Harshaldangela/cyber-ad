import React from 'react';
import styled from 'styled-components';
import { FaShieldAlt, FaBrain, FaChartLine, FaLanguage, FaGithub, FaCode } from 'react-icons/fa';

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

const FeatureGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 25px;
  margin: 25px 0;
`;

const FeatureCard = styled.div`
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
  
  svg {
    font-size: 2.5rem;
    color: ${props => props.theme.primary};
    margin-bottom: 20px;
  }
  
  h3 {
    margin: 15px 0;
    color: ${props => props.theme.text};
    font-size: 1.3rem;
  }
  
  p {
    color: ${props => props.theme.text};
    opacity: 0.8;
    line-height: 1.6;
  }
`;

const About = () => {
  return (
    <Container>
      <Section>
        <SectionHeader>
          <FaShieldAlt />
          <span>About SMS Spam Classifier</span>
        </SectionHeader>
        
        <p>
          The SMS Spam Classifier is an advanced machine learning project that not only classifies 
          SMS messages as spam or legitimate but also generates educational cyber awareness 
          advertisements when spam is detected.
        </p>
        
        <p>
          This tool helps users identify potentially harmful messages and educates them about 
          cybersecurity best practices through AI-generated content.
        </p>
      </Section>
      
      <Section>
        <SectionHeader>
          <span>Key Features</span>
        </SectionHeader>
        
        <FeatureGrid>
          <FeatureCard>
            <FaBrain />
            <h3>Machine Learning</h3>
            <p>Advanced algorithms to accurately detect spam messages</p>
          </FeatureCard>
          
          <FeatureCard>
            <FaShieldAlt />
            <h3>Cyber Awareness</h3>
            <p>AI-generated educational content for detected spam</p>
          </FeatureCard>
          
          <FeatureCard>
            <FaChartLine />
            <h3>Analytics</h3>
            <p>Visualize trends and statistics of your classifications</p>
          </FeatureCard>
          
          <FeatureCard>
            <FaLanguage />
            <h3>Multi-language</h3>
            <p>Translate awareness content to multiple languages</p>
          </FeatureCard>
        </FeatureGrid>
      </Section>
      
      <Section>
        <SectionHeader>
          <FaCode />
          <span>Technology Stack</span>
        </SectionHeader>
        
        <p>
          This project combines modern frontend technologies with powerful backend capabilities:
        </p>
        
        <ul>
          <li>React.js for the frontend interface</li>
          <li>Styled Components for styling</li>
          <li>Chart.js for data visualization</li>
          <li>Python with scikit-learn for machine learning</li>
          <li>Google's Gemini AI for content generation</li>
          <li>FastAPI for backend API</li>
        </ul>
      </Section>
    </Container>
  );
};

export default About;