import React from 'react';
import {DashboardLayout} from '../components/Layout';
import ExperimentsTable from "../components/ExperimentsTable";
import {Typography} from "@material-ui/core";

const Header = () => {
  return (
    <header className='header'>
      <Typography variant='h4'>
        Experiments configuration
      </Typography>
      <Typography variant='h6'>
        Set the metadata for your datasets
      </Typography>
    </header>
  )
}

const Experiments = ({ experiments, setExperiments, nExperimentsRows, setExperimentsRows }) => {

  return (
    <DashboardLayout>
      <div className='App'>
        <Header />
        <ExperimentsTable
          experiments={experiments}
          setExperiments={setExperiments}
          nExperimentsRows={nExperimentsRows}
          setExperimentsRows={setExperimentsRows}
        />
      </div>
    </DashboardLayout>
  )
}

export default Experiments;