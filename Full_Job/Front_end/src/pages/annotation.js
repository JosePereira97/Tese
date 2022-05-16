import React from 'react';
import {DashboardLayout} from '../components/Layout';
import { Toolbar, Typography } from "@material-ui/core";
import  Accordion  from "../components/Accordion";

export const AnnotationResults = ({ outputsFiles }) => {
  const getAnnotationResults = (files) => {
      
    let blobNumber = 0;

    return files.map(file => {
      blobNumber++;

      const fileUrl = URL.createObjectURL(file.blob)
      console.log(fileUrl)

      return (
        <Accordion key={`accordion_${blobNumber}`} title={file.name}>
          <iframe title={`iframe_${blobNumber}`} src={fileUrl} style={{width: "100%", height: "1000px"}}></iframe>
        </Accordion>
      )})
  }

  return (
    <DashboardLayout>
      <Toolbar>
        <Typography variant="h6">Annotation Results</Typography>
      </Toolbar>
      
      {getAnnotationResults(outputsFiles)}
    </DashboardLayout>
  )
}