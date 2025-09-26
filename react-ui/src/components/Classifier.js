import React, { useState } from 'react';
import styled from 'styled-components';
import { FaSearch, FaDownload, FaGlobe, FaLightbulb, FaRegFileAlt, FaChartBar } from 'react-icons/fa';

const Container = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
  
  @media (max-width: 992px) {
    grid-template-columns: 1fr;
  }
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

const TextArea = styled.textarea`
  width: 100%;
  min-height: 200px;
  padding: 15px;
  border-radius: 8px;
  border: 2px solid ${props => props.theme.border};
  background-color: ${props => props.theme.cardBackground};
  color: ${props => props.theme.text};
  font-family: inherit;
  font-size: 1rem;
  resize: vertical;
  box-sizing: border-box;
  transition: border-color 0.3s, box-shadow 0.3s;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.primary};
    box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.2);
  }
  
  &::placeholder {
    color: ${props => props.theme.text};
    opacity: 0.6;
  }
`;

const Button = styled.button`
  background: ${props => props.primary ? 
    `linear-gradient(135deg, ${props.theme.primary} 0%, #1565c0 100%)` : 
    `linear-gradient(135deg, ${props.theme.secondary} 0%, #c51162 100%)`};
  color: white;
  border: none;
  border-radius: 8px;
  padding: 14px 28px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    background: ${props => props.primary ? 
      `linear-gradient(135deg, #1565c0 0%, #0d47a1 100%)` : 
      `linear-gradient(135deg, #c51162 0%, #ad1457 100%)`};
  }
  
  &:active {
    transform: translateY(0);
  }
  
  &:disabled {
    background: #cccccc;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
  
  @media (max-width: 768px) {
    width: 100%;
    justify-content: center;
  }
`;

const ResultCard = styled.div`
  padding: 25px;
  border-radius: 12px;
  margin: 25px 0;
  border-left: 5px solid ${props => props.type === 'spam' ? props.theme.danger : props.theme.success};
  background: ${props => props.type === 'spam' ? 
    (props.theme.name === 'dark' ? 'rgba(244, 67, 54, 0.15)' : 'rgba(244, 67, 54, 0.1)') : 
    (props.theme.name === 'dark' ? 'rgba(76, 175, 80, 0.15)' : 'rgba(76, 175, 80, 0.1)')};
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
`;

const ConfidenceBar = styled.div`
  width: 100%;
  height: 10px;
  background-color: ${props => props.theme.border};
  border-radius: 5px;
  margin: 15px 0;
  overflow: hidden;
`;

const ConfidenceFill = styled.div`
  height: 100%;
  width: ${props => props.percentage}%;
  background: ${props => props.type === 'spam' ? props.theme.danger : props.theme.success};
  border-radius: 5px;
`;

const AdCard = styled.div`
  padding: 25px;
  border-radius: 12px;
  margin: 25px 0;
  border-left: 5px solid ${props => props.theme.warning};
  background: ${props => props.theme.name === 'dark' ? 'rgba(255, 152, 0, 0.15)' : 'rgba(255, 152, 0, 0.1)'};
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
`;

const Spinner = styled.div`
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: ${props => props.theme.primary};
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
  
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
`;

const LanguageSelector = styled.select`
  width: 100%;
  padding: 14px;
  border-radius: 8px;
  border: 2px solid ${props => props.theme.border};
  background-color: ${props => props.theme.cardBackground};
  color: ${props => props.theme.text};
  font-family: inherit;
  font-size: 1rem;
  margin: 15px 0;
  transition: border-color 0.3s, box-shadow 0.3s;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.primary};
    box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.2);
  }
`;

const DownloadButton = styled.a`
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, ${props => props.theme.primary} 0%, #1565c0 100%);
  color: white;
  text-decoration: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  }
  
  &:active {
    transform: translateY(0);
  }
`;

const AdContent = styled.div`
  background-color: ${props => props.theme.name === 'dark' ? 'rgba(0, 0, 0, 0.2)' : 'rgba(0, 0, 0, 0.05)'};
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
  white-space: pre-wrap;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
`;

const Classifier = ({ apiKey, addToHistory }) => {
  const [inputMessage, setInputMessage] = useState('');
  const [result, setResult] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [adContent, setAdContent] = useState('');
  const [translations, setTranslations] = useState({});
  const [selectedLanguage, setSelectedLanguage] = useState('');

  const availableLanguages = [
    { name: 'Hindi', code: 'hi' },
    { name: 'Marathi', code: 'mr' },
    { name: 'Bengali', code: 'bn' },
    { name: 'Telugu', code: 'te' },
    { name: 'Tamil', code: 'ta' },
    { name: 'Gujarati', code: 'gu' },
    { name: 'Kannada', code: 'kn' },
    { name: 'Malayalam', code: 'ml' },
    { name: 'Punjabi', code: 'pa' },
    { name: 'Urdu', code: 'ur' },
    { name: 'French', code: 'fr' },
    { name: 'Spanish', code: 'es' },
    { name: 'German', code: 'de' },
    { name: 'Arabic', code: 'ar' },
    { name: 'Chinese (Simplified)', code: 'zh' },
    { name: 'Japanese', code: 'ja' }
  ];

  const analyzeMessage = async () => {
    if (!inputMessage.trim()) {
      alert('Please enter a message to analyze');
      return;
    }

    setLoading(true);
    setResult(null);
    setConfidence(null);
    setAdContent('');
    setTranslations({});

    try {
      // Call the improved FastAPI backend for analysis
      const response = await fetch('http://localhost:8006/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: inputMessage,
          languages: apiKey ? [] : null // Only request translations if API key is provided
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Convert classification to numeric value (1 for spam, 0 for not_spam)
      const classificationResult = data.classification === 'spam' ? 1 : 0;
      
      setResult(classificationResult);
      setConfidence(data.confidence || 0);
      
      if (classificationResult === 1 && data.ad) {
        setAdContent(data.ad);
      } else if (classificationResult === 1 && data.ad_generation_error) {
        // Show error message when ad generation fails
        setAdContent(`Ad generation unavailable: ${data.ad_generation_error}`);
      }
      
      // Add to history
      addToHistory(
        inputMessage, 
        classificationResult === 1 ? 'Spam' : 'Not Spam', 
        classificationResult === 1 && data.ad ? data.ad : null
      );
    } catch (error) {
      console.error('Error analyzing message:', error);
      alert('Error analyzing message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const translateAd = async () => {
    if (!selectedLanguage || !adContent) return;
    
    setLoading(true);
    
    try {
      // Call the FastAPI backend for translation
      const response = await fetch('http://localhost:8006/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ad_text: adContent,
          languages: [selectedLanguage]
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.translations && data.translations[selectedLanguage]) {
        setTranslations(prev => ({
          ...prev,
          [selectedLanguage]: data.translations[selectedLanguage]
        }));
      }
    } catch (error) {
      console.error('Error translating ad:', error);
      alert('Error translating ad. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const downloadAd = (content, filename) => {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <Container>
      <div>
        <Section>
          <SectionHeader>
            <FaRegFileAlt />
            <span>Message Input</span>
          </SectionHeader>
          <TextArea
            placeholder="Enter the SMS message to classify..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
          />
          <Button 
            primary 
            onClick={analyzeMessage} 
            disabled={loading}
          >
            {loading ? <Spinner /> : <FaSearch />}
            {loading ? 'Analyzing...' : 'Analyze Message'}
          </Button>
        </Section>
        
        {result !== null && (
          <Section>
            <SectionHeader>
              <span>Analysis Results</span>
            </SectionHeader>
            <ResultCard type={result === 1 ? 'spam' : 'not-spam'}>
              <h3>{result === 1 ? '🚨 SPAM DETECTED' : '✅ NOT SPAM'}</h3>
              <p>
                This message has been classified as <strong>{result === 1 ? 'spam' : 'legitimate'}</strong>.
              </p>
              {confidence !== null && (
                <div>
                  <p><strong>Confidence: {(confidence * 100).toFixed(1)}%</strong></p>
                  <ConfidenceBar>
                    <ConfidenceFill 
                      percentage={confidence * 100} 
                      type={result === 1 ? 'spam' : 'not-spam'}
                    />
                  </ConfidenceBar>
                </div>
              )}
            </ResultCard>
            
            {result === 1 && adContent && (
              <AdCard>
                <SectionHeader>
                  <FaLightbulb />
                  <span>Cyber Awareness Ad</span>
                </SectionHeader>
                <AdContent>
                  {adContent}
                </AdContent>
                {/* Only show download button if we have a real ad (not an error message) */}
                {!adContent.includes("Ad generation unavailable") && (
                  <DownloadButton 
                    href="#" 
                    onClick={(e) => {
                      e.preventDefault();
                      downloadAd(adContent, `cyber_awareness_ad_${new Date().getTime()}.txt`);
                    }}
                  >
                    <FaDownload />
                    Download Ad Content
                  </DownloadButton>
                )}
                
                {/* Only show translation options if we have a real ad */}
                {!adContent.includes("Ad generation unavailable") && (
                  <>
                    <h4><FaGlobe /> Translate this Ad</h4>
                    <LanguageSelector 
                      value={selectedLanguage} 
                      onChange={(e) => setSelectedLanguage(e.target.value)}
                    >
                      <option value="">Select a language</option>
                      {availableLanguages.map(lang => (
                        <option key={lang.code} value={lang.name}>
                          {lang.name}
                        </option>
                      ))}
                    </LanguageSelector>
                    <Button onClick={translateAd} disabled={loading || !selectedLanguage}>
                      {loading ? 'Translating...' : 'Translate'}
                    </Button>
                    
                    {translations[selectedLanguage] && (
                      <div style={{ marginTop: '25px' }}>
                        <h4>{selectedLanguage} Translation</h4>
                        <AdContent>
                          {translations[selectedLanguage]}
                        </AdContent>
                        <DownloadButton 
                          href="#" 
                          onClick={(e) => {
                            e.preventDefault();
                            downloadAd(translations[selectedLanguage], `cyber_awareness_ad_${selectedLanguage}_${new Date().getTime()}.txt`);
                          }}
                        >
                          <FaDownload />
                          Download {selectedLanguage} Version
                        </DownloadButton>
                      </div>
                    )}
                  </>
                )}
              </AdCard>
            )}
          </Section>
        )}
      </div>
      
      <div>
        <Section>
          <SectionHeader>
            <FaChartBar />
            <span>Model Information</span>
          </SectionHeader>
          <div>
            <h3>Improved Classification Model</h3>
            <p>
              This application now uses an enhanced machine learning model with the following improvements:
            </p>
            <ul>
              <li>Advanced text preprocessing (URL/email/phone number removal)</li>
              <li>TF-IDF with n-grams (unigrams and bigrams)</li>
              <li>Logistic Regression classifier with optimized parameters</li>
              <li>Confidence scoring for each prediction</li>
              <li>Better handling of edge cases</li>
            </ul>
            
            <h3>Performance Metrics</h3>
            <ul>
              <li>Accuracy: ~97.7%</li>
              <li>Precision: ~95.0%</li>
              <li>Recall: ~86.3%</li>
              <li>F1-Score: ~90.4%</li>
            </ul>
            
            <h3>How to Identify Spam</h3>
            <ul>
              <li>Urgent or threatening language</li>
              <li>Requests for personal information</li>
              <li>Suspicious links or phone numbers</li>
              <li>Unexpected prizes or offers</li>
              <li>Poor grammar or spelling</li>
            </ul>
          </div>
        </Section>
      </div>
    </Container>
  );
};

export default Classifier;