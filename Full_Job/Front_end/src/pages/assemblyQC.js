import React, { useState, useEffect } from 'react';
import { DashboardLayout } from '../components/Layout';
import { Toolbar, Typography } from "@material-ui/core";
import * as Papa from "papaparse"
import DataTable from 'react-data-table-component'
import Accordion from "../components/Accordion";

const Main = ({ outputsFolder }) => {
  const [tables, setTables] = useState([])
  let auxTables = []

  const updateTables = (file) => {
    auxTables.push(file)
    
    if(outputsFolder.length === auxTables.length){
      setTables(auxTables)
    }
  }

  const readCsv = (csvUrl, fileName) => {
    Papa.parse(csvUrl, {
      download: true,
      header: true,
      complete: function (results) {
        results.data.pop()
        updateTables({ fileContent: results.data, fileName });
      }
    })
  }

  useEffect(() => {
    outputsFolder.forEach(file => {
      let csvUrl = URL.createObjectURL(file.blob)
      readCsv(csvUrl, file.name)
    })
  });

  let tableCounter = 0

  const capitalizeFirstLetter = (text) => {
    return text.charAt(0).toUpperCase() + text.slice(1)
  }

  const getColumnNamesFromData = (fileContent) =>{
      return Object.keys(fileContent[0]).map(key =>{
        return({name: capitalizeFirstLetter(key), selector: key, sortable: true})
      })
  }

  return (
    <main className='main'>
      <Toolbar>
        <Typography variant="h6">Quality check reports from assembly</Typography>
      </Toolbar>

      {tables.map(file => {
        tableCounter++;
        return (
          <Accordion key={`accordion_${tableCounter}`} title={file.fileName}>
            <DataTable
              style={{ width: "100%", height: "100%" }}
              pagination
              noHeader
              columns={getColumnNamesFromData(file.fileContent)}
              data={file.fileContent}
            />
          </Accordion>)
      })}

    </main>
  )
}

const AssemblyQC = ({ outputsFolder }) => {
  return (
    <DashboardLayout>
      <Main
        outputsFolder={outputsFolder}
      />
    </DashboardLayout>
  )
}

export default AssemblyQC;