import React from 'react';

import {DashboardLayout} from '../components/Layout';
import {Button, Card, CardContent, Divider, Typography} from "@material-ui/core";
import {DiGithubBadge} from "react-icons/di";
import {SiAnaconda, SiReadthedocs} from "react-icons/si";
import Avatar from "@material-ui/core/Avatar";
import {makeStyles} from "@material-ui/core/styles";
import logo from '../public/mosca_logo.png'

const useStyles = makeStyles({
  root: {
    marginTop: "10px",
    marginBottom: "10px"
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
        MOSCA
      </Typography>
      <Typography variant='h6'>
        Meta-Omics Software for Community Analysis
      </Typography>
    </header>
  )
}

const Main = () => {
  const classes = useStyles();

  return (
    <>
      <Card className={classes.root}>
        <CardContent>
          <img src={logo} alt="Logo" width={"300rem"} />
        </CardContent>
      </Card>

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
            href="https://github.com/iquasere/MOSCA/wiki"
            target="__blank"
            className={classes.littleCardsStyle}
            startIcon={<SiReadthedocs size="2em" />}
          >
            Wiki
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
    </>
  )
}

const ProjectPage = () => {
  return (
    <DashboardLayout>
      <div className='App'>
        <Header/>
        <Main/>
      </div>
    </DashboardLayout>
  )
}

export default ProjectPage;