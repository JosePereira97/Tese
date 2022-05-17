import React, { useState } from 'react';
import { DashboardLayout } from '../components/Layout';
import { Button, Toolbar, Typography } from "@material-ui/core";
import * as zip from "@zip.js/zip.js";
import $ from 'jquery'
import * as Papa from "papaparse"
import axios from "axios"
import {format} from "date-fns"
import {useEffect} from "react"
import {useTable} from "react-table"

zip.configure({ useWebWorkers: false });

const baseUrl = "http://localhost:5000"



export const LoadResults = ({ outputsFiles, setOutputsFiles, onConfigOverwrite, setExperiments, setExperimentsRows }) => {

  const GetResults = async () => {
    const results = await axios.get(`${baseUrl}/get_all_user_files`)
    const {names} = results.data
    console.log(results)
    console.log(results.data)
    console.log(names)
    setMy_analyses(names)
  }

  const [My_analyses, setMy_analyses] = useState([])
  
  useEffect(() => {
    GetResults();
  }, [])

  return (
    <DashboardLayout>
      <Toolbar>
        <Typography variant="h6">List of all the analyses made</Typography>
      </Toolbar>
      <section>
        <ul>
          {My_analyses.map(results =>{
            return (
              <li>{results}</li>
            )
          })}
        </ul>
      </section>
    </DashboardLayout>
  )


}