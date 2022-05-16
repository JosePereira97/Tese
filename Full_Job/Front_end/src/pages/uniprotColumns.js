import React from 'react';

import {DashboardLayout} from '../components/Layout';
import {Card, Typography} from "@material-ui/core";
import UniprotAccordion from "../components/UniprotAccordion";
import {uniprotColumns} from "../utils/uniprotColumns"

const Main = ({ uniprotList, onChange }) => {

  return (
    <main className='main'>
      <form className='form' >
        <Card >
          <UniprotAccordion
            uniprotList={uniprotList}
            onChange={onChange}
            uniprotPossibilities={uniprotColumns}
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
        UniProt columns
      </Typography>
    </header>
  )
}

const UniprotColumns = ({ uniprotList, onChange }) => {
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

export default UniprotColumns;