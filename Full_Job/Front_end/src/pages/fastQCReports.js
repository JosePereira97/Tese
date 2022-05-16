import React from 'react';
import { DashboardLayout } from '../components/Layout';
import { Toolbar, Typography } from "@material-ui/core";
import Accordion from "../components/Accordion";


export const FastQCFiles = ({ outputsFiles }) => {
  const getJsxFromFiles = (files) => {
    let blobNumber = 0;

    return files.map(file => {
      blobNumber++;

      const fileUrl = URL.createObjectURL(file.blob)

      return <Accordion key={`accordion_${blobNumber}`} title={file.name}>
        <iframe title={`iframe_${blobNumber}`} src={fileUrl} style={{ width: "100%", height: "1000px" }}></iframe>
      </Accordion>
    })
  }

  return (
    <DashboardLayout outputsFiles={outputsFiles}>
      <Toolbar>
        <Typography variant="h6">FastQC Reports</Typography>
      </Toolbar>
      
      {getJsxFromFiles(outputsFiles.qcReports)}
    </DashboardLayout>
  )
}