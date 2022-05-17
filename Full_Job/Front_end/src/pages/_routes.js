import React from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";

import ProjectPage from "./project";
import MembersPage from "./members";
import AboutPage from "./about";
import TeamsPage from "./teams";
import HomePage from "./home";
import Config from "./config"
import Experiments from "./experiments";
import UniprotColumns from "./uniprotColumns";
import UniprotDatabases from "./uniprotDatabases"
import KeggMaps from "./keggmaps";
//import {LoadResults} from "./results";
import {FastQCFiles} from "./fastQCReports";
import AssemblyQC from "./assemblyQC";
import {AnnotationResults} from './annotation';
import {DifferentialResults} from './differentialExpressionResults'
import {KeggmapsResults} from './keggmapsResults'
import EntryReports from "./entryReport";
import GeneralReports from "./generalReports";
import ProteinReports from "./proteinReports";
import { LoadResults } from "./results";

const Routes = ({ configData, onConfigChange, onConfigOverwrite, experiments, setExperiments,
                  nExperimentsRows, setExperimentsRows, hasMt, toggleHasMt, hasMp, toggleHasMp,
                  outputsFiles, setOutputsFiles }) => {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/MOSGUITO/general-configuration">
          <Config
            configData={configData}
            onConfigChange={onConfigChange}
            onConfigOverwrite={onConfigOverwrite}
            hasMt={hasMt}
            toggleHasMt={toggleHasMt}
            hasMp={hasMp}
            toggleHasMp={toggleHasMp}
          />
        </Route>

        <Route path="/MOSGUITO/experiments">
          <Experiments
            experiments={experiments}
            setExperiments={setExperiments}
            nExperimentsRows={nExperimentsRows}
            setExperimentsRows={setExperimentsRows}
          />
        </Route>

        <Route path="/MOSGUITO/uniprot-columns">
          <UniprotColumns
            uniprotList={configData.upimapiColumns}
            onChange={(value) => onConfigChange('upimapiColumns', value)}
          />
        </Route>

        <Route path="/MOSGUITO/uniprot-databases">
          <UniprotDatabases
            uniprotList={configData.upimapiDatabases}
            onChange={(value) => onConfigChange('upimapiDatabases', value)}
          />
        </Route>

        <Route path="/MOSGUITO/keggmaps">
          <KeggMaps
            configData={configData}
            onConfigChange={onConfigChange}
          />
        </Route>

        <Route path="/MOSGUITO/about">
        </Route>

        <Route path="/MOSGUITO/members">
          <MembersPage />
        </Route>

        <Route path="/MOSGUITO/project">
          <ProjectPage />
        </Route>

        <Route path="/MOSGUITO/about">
          <AboutPage />
        </Route>

        <Route path="/MOSGUITO/another/teams">
          <TeamsPage />
        </Route>

        <Route path="/MOSGUITO/results">
          <LoadResults
            outputsFiles={outputsFiles}
            setOutputsFiles={setOutputsFiles}
            onConfigOverwrite ={onConfigOverwrite}
            setExperiments = {setExperiments}
            setExperimentsRows = {setExperimentsRows}
          />
        </Route>

        <Route path="/MOSGUITO/load-results">
          <LoadResults
            outputsFiles={outputsFiles}
            setOutputsFiles={setOutputsFiles}
            onConfigChange ={onConfigChange}
            setExperiments = {setExperiments}
            setExperimentsRows = {setExperimentsRows}
          />
        </Route>

        <Route path="/MOSGUITO/fastqc-reports">
          <FastQCFiles
            outputsFiles={outputsFiles}
          />
        </Route>

        <Route path="/MOSGUITO/assembly-qc">
          <AssemblyQC
            outputsFolder={outputsFiles.asReports}
          />
        </Route>

        <Route path = '/MOSGUITO/annotation-results'>
          <AnnotationResults
            outputsFiles = {outputsFiles.KronaPlots}
          />
        </Route>

        <Route path = '/MOSGUITO/differential-analysis'>
          <DifferentialResults
            outputsFiles = {outputsFiles.Heatmaps}
          />
        </Route>
        
        <Route path = '/MOSGUITO/keggmaps-results'>
          <KeggmapsResults
            outputsFiles = {outputsFiles.KEGGMaps}
          />
        </Route>

        <Route path = '/MOSGUITO/entry-reports'>
          <EntryReports
            outputsFolder = {outputsFiles.entryReport}
          />
        </Route>

        <Route path = '/MOSGUITO/general-reports'>
          <GeneralReports
            outputsFolder = {outputsFiles.generalReport}
          />
        </Route>

        <Route path = '/MOSGUITO/protein-reports'>
          <ProteinReports
            outputsFolder = {outputsFiles.proteinReport}
          />
        </Route>

        <Route path="/MOSGUITO">
          <HomePage />
        </Route>
      </Switch>
    </BrowserRouter>
  );
};

export default Routes;
