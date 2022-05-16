import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {DashboardLayout} from '../components/Layout';
import {Card, CardContent, Divider, Typography} from "@material-ui/core";
import { DiGithubBadge } from "react-icons/di"
import { SiAnaconda } from "react-icons/si"
import { Button } from '@material-ui/core';
import Avatar from "@material-ui/core/Avatar";

const useStyles = makeStyles({
  root: {
    maxWidth: "50%"
  },
  littleCardsStyle: {
    marginRight: '10px'
  },
  mosguitoDivider: {
    marginTop: '40px',
    margin: '1rem 0'
  }
});

const Header = () => {
  return (
    <header className='header'>
      <Typography variant='h4'>
        MOSGUITO
      </Typography>
      <Typography variant='h6'>
        MOSca's GUI TO perform meta-omics analyses
      </Typography>
    </header>
  )
}

const Main = () => {
  const classes = useStyles();

  return (
    <main className='main'>
      <div className='rowC'>
        <Card className={classes.root}>
          <CardContent>
            <b>MOSCA</b> is a command-line pipeline for performing metagenomics, metatranscriptomics and metaproteomics analysis.
            <Divider style={{ margin: '1rem 0' }} />
            <Button
              variant="contained"
              href="https://github.com/iquasere/MOSCA"
              target="__blank"
              className={classes.littleCardsStyle}
              startIcon={<DiGithubBadge size="2em"/>}
            >
              GitHub
            </Button>
            <Button
              variant="contained"
              href="https://anaconda.org/bioconda/MOSCA"
              target="__blank"
              className={classes.littleCardsStyle}
              startIcon={<SiAnaconda size="2em" />}
            >
              Bioconda
            </Button>
            <Button
              variant="contained"
              href="https://bio.tools/mosca"
              target="__blank"
              startIcon={<Avatar src={"https://user-images.githubusercontent.com/1506863/49924558-986f5d80-feae-11e8-8398-7cddbf834ffe.png"} size="2em" />}
            >
              bio.tools
            </Button>
          </CardContent>
        </Card>
        <Card className={classes.root}>
          <CardContent>
            <b>MOSGUITO</b> is the graphical interface for configuring MOSCA and visualizing its results.
            <Divider className={classes.mosguitoDivider} />
            <Button
              variant="contained"
              href="https://github.com/iquasere/MOSGUITO"
              target="__blank"
              className={classes.littleCardsStyle}
              startIcon={<DiGithubBadge size="2em"/>}
            >
              GitHub
            </Button>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}

const HomePage = () => {
  return (
    <DashboardLayout>
      <div className='App'>
        <Header />
        <Main />
      </div>
    </DashboardLayout>
  )
}

export default HomePage;