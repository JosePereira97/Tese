import React from 'react';

import {DashboardLayout} from '../components/Layout';
import { Card, Typography } from "@material-ui/core";
import KeggMapsAccordion from "../components/KeggMapsAccordion";

const Main = ({ configData, onConfigChange }) => {

  return (
    <main className='main'>
      <form className='form' >
        <Card>
      <KeggMapsAccordion
        keggMapList={configData.keggcharterMaps}
        onChange={(value) => onConfigChange('keggcharterMaps', value)}
      />
      </Card>
      </form>
    </main>
  )
}

const Header = () => {
  return (
    <header className='header'>
      <Typography variant='h4'>
        KEGG metabolic maps
      </Typography>
    </header>
  )
}

const KeggMaps = ({ configData, onConfigChange }) => {
  return (
    <DashboardLayout>
      <div className='App'>
      <Header />
      <Main
        configData={configData}
        onConfigChange={onConfigChange}
      />
      </div>
    </DashboardLayout>
  )
}

export default KeggMaps;