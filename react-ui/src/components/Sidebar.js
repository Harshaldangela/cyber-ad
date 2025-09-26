import React from 'react';
import styled from 'styled-components';
import { FaHome, FaHistory, FaInfoCircle } from 'react-icons/fa';

const SidebarContainer = styled.aside`
  width: 250px;
  background-color: ${props => props.theme.sidebarBackground};
  color: ${props => props.theme.text};
  height: calc(100vh - 60px);
  position: fixed;
  top: 60px;
  left: 0;
  overflow-y: auto;
  border-right: 1px solid ${props => props.theme.border};
  transition: transform 0.3s ease;
  transform: translateX(${props => props.isOpen ? '0' : '-100%'});
  z-index: 999;
`;

const SidebarMenu = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const MenuItem = styled.li`
  padding: 0;
`;

const MenuLink = styled.a`
  display: flex;
  align-items: center;
  padding: 15px 20px;
  text-decoration: none;
  color: ${props => props.theme.text};
  transition: background-color 0.3s;
  border-left: 3px solid transparent;
  
  &:hover {
    background-color: rgba(0, 0, 0, 0.1);
  }
  
  &.active {
    background-color: rgba(25, 118, 210, 0.1);
    border-left-color: ${props => props.theme.primary};
    font-weight: 500;
  }
  
  svg {
    margin-right: 10px;
    font-size: 1.2rem;
  }
`;

const Sidebar = ({ isOpen }) => {
  return (
    <SidebarContainer isOpen={isOpen}>
      <SidebarMenu>
        <MenuItem>
          <MenuLink href="/">
            <FaHome />
            <span>Classifier</span>
          </MenuLink>
        </MenuItem>
        {/* Commented out history link */}
        {/* <MenuItem>
          <MenuLink href="/history">
            <FaHistory />
            <span>History</span>
          </MenuLink>
        </MenuItem> */}
        <MenuItem>
          <MenuLink href="/about">
            <FaInfoCircle />
            <span>About</span>
          </MenuLink>
        </MenuItem>
      </SidebarMenu>
      
      <div style={{ padding: '20px', marginTop: 'auto' }}>
        <h3>About SMS Spam</h3>
        <p>
          SMS spam (or "smishing") is a growing threat that can lead to financial loss, 
          identity theft, and privacy breaches. This tool helps identify and educate about these threats.
        </p>
      </div>
    </SidebarContainer>
  );
};

export default Sidebar;