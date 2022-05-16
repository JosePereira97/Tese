import React from 'react';

import {DashboardLayout} from '../components/Layout';
import {Card, Typography} from "@material-ui/core";
import UniprotAccordion from "../components/UniprotAccordion";
import {uniprotDatabases} from "../utils/uniprotDatabases"

const Main = ({ uniprotList, onChange }) => {

  return (
    <main className='main'>
      <form className='form' >
        <Card>
        <UniprotAccordion
          uniprotList={uniprotList}
          onChange={onChange}
          uniprotPossibilities={uniprotDatabases}
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
        UniProt databases
      </Typography>
    </header>
  )
}

const UniprotDatabases = ({ uniprotList, onChange }) => {
  return (
    <DashboardLayout>
      <div className='App'>
      <Header />
      <Main
        uniprotList={uniprotList}
        onChange={onChange}
      />
      </div>
    </DashboardLayout>
  )
}

export default UniprotDatabases;