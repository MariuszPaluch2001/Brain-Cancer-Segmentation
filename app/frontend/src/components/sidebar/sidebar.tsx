import React from 'react';
import {
  CDBSidebar,
  CDBSidebarContent,
  CDBSidebarHeader,
  CDBSidebarMenu,
  CDBSidebarMenuItem,
} from 'cdbreact';

const Sidebar = () => {
  return (
    <div
    style={{ display: 'flex', height: '100vh', overflow: 'scroll initial' }}
  >
      <CDBSidebar className={''} textColor={''} backgroundColor={'#eeeeee'} breakpoint={0} toggled={false} minWidth={'30vh'} maxWidth={'30vh'}>
        <CDBSidebarHeader prefix={<i className="fa fa-bars" />}>Brain MRI</CDBSidebarHeader>
        <CDBSidebarContent>
          <CDBSidebarMenu>
            <CDBSidebarMenuItem icon="home">Home</CDBSidebarMenuItem>
            <CDBSidebarMenuItem icon="image">MRI & results</CDBSidebarMenuItem>
            <CDBSidebarMenuItem icon="robot" iconType="solid">
              Models
            </CDBSidebarMenuItem>
          </CDBSidebarMenu>
        </CDBSidebarContent>
      </CDBSidebar>
  </div>
  );
};

export default Sidebar;