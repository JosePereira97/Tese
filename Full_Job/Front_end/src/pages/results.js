import React from 'react';
import { DashboardLayout } from '../components/Layout';
import { Button, Toolbar, Typography } from "@material-ui/core";
import * as zip from "@zip.js/zip.js";
import $ from 'jquery'
import * as Papa from "papaparse"
zip.configure({ useWebWorkers: false });

const treatName = (name) =>{
  let resultingString = name.split('/')
  resultingString = resultingString[resultingString.length-1]
  resultingString = resultingString.split('.')
  return(resultingString[0])
}

export let ResultsDisposition = false;

async function ObtainBlobArray(event){
  const file = event.target.files[0];
  const blobReader = new zip.BlobReader(file);
  const zipReader = new zip.ZipReader (blobReader);

  const entries = await zipReader.getEntries();

  let KronaPlotsResults = [];
  let FastQCReports = [];
  let DifferentailExpressionResults = [];
  let KEGGMapsResults = [];
  let Assembly = [];
  let entry = [];
  let configFile = [];
  let exper = [];
  let general = [];
  let protein = [];

  for(let i = 0; i < entries.length; i++){
    if (entries[i].directory === false && entries[i].compressedSize !== 0){
      if(entries[i].filename.includes('Preprocess')){
        const blobFastQC = await entries[i].getData(new zip.BlobWriter(['text/html']))
        let fastQcName = treatName(entries[i].filename)
        FastQCReports.push({name: fastQcName, blob: blobFastQC})
      }
    if(entries[i].filename.includes('Annotation')){
      const blobKronaPlots = await entries[i].getData(new zip.BlobWriter(['text/html']))
      let kronaPlotsNames = treatName(entries[i].filename)
      KronaPlotsResults.push({name: kronaPlotsNames, blob: blobKronaPlots})
    }
    if(entries[i].filename.includes('Differential expression analysis')){
      const blobHeatmaps = await entries[i].getData(new zip.BlobWriter(['image/jpeg']))
      let heatMapsNames = treatName(entries[i].filename)
      DifferentailExpressionResults.push({name: heatMapsNames, blob:blobHeatmaps})

    }
    if(entries[i].filename.includes('KEGGMaps')){
      const blobKEGGMaps = await entries[i].getData(new zip.BlobWriter(['image/png']))
      let keggMaps = treatName(entries[i].filename)
      let number = KEGGMapsResults.length
      KEGGMapsResults.push({name:[number,keggMaps],blob:blobKEGGMaps})

    }
    if(entries[i].filename.includes('Assembly')){
      const AssemblyReports = await entries[i].getData(new zip.BlobWriter(['text/tab-separated-values']))
      let assemblyName = treatName(entries[i].filename)
      Assembly.push({name: assemblyName, blob: AssemblyReports})
    }
    if(entries[i].filename.includes('Entry')){
      const entryReport = await entries[i].getData(new zip.BlobWriter(['text/tab-separated-values']))
      let entryName = treatName(entries[i].filename)
      entry.push({name: entryName, blob: entryReport})
    }
    if(entries[i].filename.includes('config')){
      console.log('entrou')
      const config = await entries[i].getData(new zip.BlobWriter(['application/json']))
      console.log(config)
      const fileUrl = URL.createObjectURL(config)
      console.log(fileUrl)
      $.getJSON(fileUrl, function(json){
        exper = json.experiments
        delete json.experiments
        configFile = json
        console.log(configFile)
      })
      console.log('caguei')
    }
    if(entries[i].filename.includes('experiments')){
      const exp = await entries[i].getData(new zip.BlobWriter(['text/tab-separated-values']))
      exper = exp
    }
    if(entries[i].filename.includes('General')){
      const genReport = await entries[i].getData(new zip.BlobWriter(['text/tab-separated-values']))
      let genName = treatName(entries[i].filename)
      general.push({name: genName, blob: genReport})

    }
    if(entries[i].filename.includes('Protein')){
      const proteinReport = await entries[i].getData(new zip.BlobWriter(['text/tab-separated-values']))
      let protName = treatName(entries[i].filename)
      protein.push({name: protName, blob: proteinReport})
    }}
  }
  await zipReader.close()

  return [{
    qcReports: FastQCReports,
    KronaPlots: KronaPlotsResults,
    Heatmaps: DifferentailExpressionResults,
    KEGGMaps: KEGGMapsResults,
    asReports: Assembly,
    entryReport: entry,
    generalReport: general,
    proteinReport: protein
  }, configFile, exper]
}


const Main = ({ outputsFiles, setOutputsFiles, onConfigOverwrite, setExperiments, setExperimentsRows }) => {

  const snakeToCamelCase = str => {
    return str.replace(/([-_][a-z])/ig, ($1) => {
      return $1.toUpperCase()
        .replace('-', '')
        .replace('_', '');
    });
  };

  const handleUploadClick = () => {
    ResultsDisposition = true
  }
  const handleZipChange = async (event) => {
    let Output = await ObtainBlobArray(event)
    setOutputsFiles(Output[0])
    Object.keys(Output[1]).map(
      (key) => delete Object.assign(Output[1], {[snakeToCamelCase(key)]: Output[1][key]}))
    onConfigOverwrite(Output[1])
    
    const readCsv = (csvUrl)=>{
      Papa.parse(csvUrl,{
        download: true,
        header: true,
        complete: function (results) {
            results.data.pop()
            let newData = results.data
            setExperiments(newData);
            setExperimentsRows(Object.keys(newData).length)
        }
    })
    }
    setExperiments(Output[2])
    setExperimentsRows(Output[2].length)
  }
  return (
    <>
      <Button
        variant='contained'
        color='secondary'
        component="label"
        onClick={handleUploadClick}
      >
        Select results' ZIP archive
        <input
          type="file"
          accept='application/zip'
          onChange={handleZipChange}
          hidden
        />
      </Button>
    </>
  )
};

export const LoadResults = ({ outputsFiles, setOutputsFiles, onConfigOverwrite, setExperiments, setExperimentsRows }) => {
  return (
    <DashboardLayout>
      <Toolbar>
        <Typography variant="h6">MOSCA results page</Typography>
      </Toolbar>
      <Main
        outputsFiles={outputsFiles}
        setOutputsFiles={setOutputsFiles}
        onConfigOverwrite = {onConfigOverwrite}
        setExperiments = {setExperiments}
        setExperimentsRows = {setExperimentsRows}
      />
    </DashboardLayout>
  )
}
