import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled, { ThemeProvider, createGlobalStyle } from 'styled-components';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Classifier from './components/Classifier';
// import History from './components/History';  // Commented out history
import About from './components/About';
import './App.css';

// Global styles and theme
const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
      'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
      sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: ${props => props.theme.background};
    color: ${props => props.theme.text};
    transition: background-color 0.3s, color 0.3s;
  }
`;

const theme = {
  light: {
    background: '#f8f9fa',
    text: '#333',
    primary: '#1976d2',
    secondary: '#f50057',
    success: '#4caf50',
    danger: '#f44336',
    warning: '#ff9800',
    cardBackground: '#ffffff',
    sidebarBackground: '#ffffff',
    border: '#e0e0e0'
  },
  dark: {
    background: '#121212',
    text: '#ffffff',
    primary: '#90caf9',
    secondary: '#f50057',
    success: '#69f0ae',
    danger: '#ff5252',
    warning: '#ffd740',
    cardBackground: '#1e1e1e',
    sidebarBackground: '#1e1e1e',
    border: '#424242'
  }
};

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: ${props => props.theme.background};
  color: ${props => props.theme.text};
`;

const MainContent = styled.main`
  display: flex;
  flex: 1;
  margin-top: 60px;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const ContentArea = styled.div`
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  margin-left: ${props => props.sidebarOpen ? '250px' : '0'};
  transition: margin-left 0.3s ease;
  background-color: ${props => props.theme.background};
  color: ${props => props.theme.text};
  
  @media (max-width: 768px) {
    margin-left: 0;
  }
`;

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [apiKey, setApiKey] = useState('');
  // const [history, setHistory] = useState([]);  // Commented out history
  // const [stats, setStats] = useState({ spam: 0, notSpam: 0 });  // Commented out stats
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Load data from localStorage on initial render
  useEffect(() => {
    const savedApiKey = localStorage.getItem('apiKey');
    // const savedHistory = localStorage.getItem('history');  // Commented out history
    const savedDarkMode = localStorage.getItem('darkMode') === 'true';
    const savedSidebarOpen = localStorage.getItem('sidebarOpen') === 'true';
    
    if (savedApiKey) setApiKey(savedApiKey);
    // if (savedHistory) {  // Commented out history
    //   try {
    //     const parsedHistory = JSON.parse(savedHistory);
    //     setHistory(parsedHistory);
    //     
    //     // Calculate initial stats
    //     const spamCount = parsedHistory.filter(item => item.result === 'Spam').length;
    //     setStats({
    //       spam: spamCount,
    //       notSpam: parsedHistory.length - spamCount
    //     });
    //   } catch (e) {
    //     console.error('Error parsing history:', e);
    //     setHistory([]);
    //   }
    // }
    setDarkMode(savedDarkMode);
    setSidebarOpen(savedSidebarOpen);
  }, []);

  // Save data to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('apiKey', apiKey);
  }, [apiKey]);

  // useEffect(() => {  // Commented out history
  //   localStorage.setItem('history', JSON.stringify(history));
  // }, [history]);

  useEffect(() => {
    localStorage.setItem('darkMode', darkMode);
  }, [darkMode]);

  useEffect(() => {
    localStorage.setItem('sidebarOpen', sidebarOpen);
  }, [sidebarOpen]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // const addToHistory = (message, result, adContent = null) => {  // Commented out history
  //   const newEntry = {
  //     id: Date.now(),
  //     timestamp: new Date().toISOString(),
  //     message,
  //     result,
  //     adContent
  //   };
  //   
  //   const updatedHistory = [newEntry, ...history];
  //   setHistory(updatedHistory);
  //   
  //   // Update stats
  //   setStats(prevStats => ({
  //     spam: result === 'Spam' ? prevStats.spam + 1 : prevStats.spam,
  //     notSpam: result === 'Not Spam' ? prevStats.notSpam + 1 : prevStats.notSpam
  //   }));
  // };

  const currentTheme = darkMode ? theme.dark : theme.light;

  return (
    <ThemeProvider theme={currentTheme}>
      <GlobalStyle />
      <AppContainer>
        <Router>
          <Header 
            darkMode={darkMode} 
            toggleDarkMode={toggleDarkMode} 
            apiKey={apiKey}
            setApiKey={setApiKey}
            toggleSidebar={toggleSidebar}
            sidebarOpen={sidebarOpen}
          />
          <MainContent>
            <Sidebar isOpen={sidebarOpen} />
            <ContentArea sidebarOpen={sidebarOpen}>
              <Routes>
                <Route 
                  path="/" 
                  element={
                    <Classifier 
                      apiKey={apiKey} 
                      // addToHistory={addToHistory}  // Commented out history
                    />
                  } 
                />
                {/* <Route  // Commented out history
                  path="/history" 
                  element={<History history={history} />} 
                /> */}
                <Route path="/about" element={<About />} />
              </Routes>
            </ContentArea>
          </MainContent>
        </Router>
      </AppContainer>
    </ThemeProvider>
  );
}

export default App;