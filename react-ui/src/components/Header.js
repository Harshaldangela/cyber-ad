import React from 'react';
import styled from 'styled-components';
import { FaBars, FaSun, FaMoon, FaShieldAlt } from 'react-icons/fa';

const HeaderContainer = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: ${props => props.theme.cardBackground};
  color: ${props => props.theme.text};
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  border-bottom: 1px solid ${props => props.theme.border};
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.5rem;
  font-weight: bold;
`;

const Nav = styled.nav`
  display: flex;
  gap: 20px;
  
  @media (max-width: 768px) {
    display: none;
  }
`;

const NavLink = styled.a`
  color: ${props => props.theme.text};
  text-decoration: none;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: rgba(0, 0, 0, 0.1);
  }
  
  &.active {
    background-color: ${props => props.theme.primary};
    color: white;
  }
`;

const Controls = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
`;

const ApiKeyInput = styled.input`
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid ${props => props.theme.border};
  background-color: ${props => props.theme.cardBackground};
  color: ${props => props.theme.text};
  
  @media (max-width: 768px) {
    width: 120px;
  }
`;

const IconButton = styled.button`
  background: none;
  border: none;
  color: ${props => props.theme.text};
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: rgba(0, 0, 0, 0.1);
  }
`;

const MobileMenuButton = styled(IconButton)`
  display: none;
  
  @media (max-width: 768px) {
    display: flex;
  }
`;

const Header = ({ darkMode, toggleDarkMode, apiKey, setApiKey, toggleSidebar, sidebarOpen }) => {
  return (
    <HeaderContainer>
      <Logo>
        <IconButton onClick={toggleSidebar}>
          <FaBars />
        </IconButton>
        <FaShieldAlt />
        <span>SMS Spam Classifier</span>
      </Logo>
      
      <Nav>
        <NavLink href="/">Classifier</NavLink>
        <NavLink href="/history">History</NavLink>
        <NavLink href="/about">About</NavLink>
      </Nav>
      
      <Controls>
        <ApiKeyInput
          type="password"
          placeholder="API Key"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
        <IconButton onClick={toggleDarkMode}>
          {darkMode ? <FaSun /> : <FaMoon />}
        </IconButton>
        <MobileMenuButton onClick={toggleSidebar}>
          <FaBars />
        </MobileMenuButton>
      </Controls>
    </HeaderContainer>
  );
};

export default Header;