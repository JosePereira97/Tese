import React, { useState, useEffect, useMemo } from 'react';
import { DashboardLayout } from '../components/Layout';
import { Button, Toolbar, Typography } from "@material-ui/core";
import * as Papa from "papaparse"
import DataTable from 'react-data-table-component'
import FilterComponent from './filterDataTest';
import TSV from "tsv";
import download from "../utils/download";

const Main = ({ outputsFolder }) => {

    const replaceArray = (array) =>{
        return array.map((dic)=>{
            const newReplace = {}
            for(const [key, value] of Object.entries(dic)){
                let newKey = key.replaceAll('.', '/').replaceAll('[','(').replaceAll(']',')').replaceAll(':','_')
                newReplace[newKey] = value
            }
            return newReplace
        })
    }

    const [table, setTable] = useState([])
    let auxTables = []

    const updateTables = (file) => {
        auxTables.push(file)

        if (outputsFolder.length === auxTables.length) {
            setTable(auxTables)
        }
    }
    const readCsv = (csvUrl, fileName) => {
        Papa.parse(csvUrl, {
            download: true,
            header: true,
            complete: function (results) {
                results.data.pop()
                let parse = replaceArray(results.data)
                updateTables({ fileContent: parse, fileName });
            }
        })
    }

    useEffect(() => {
        outputsFolder.forEach(file => {
          let csvUrl = URL.createObjectURL(file.blob)
          readCsv(csvUrl, file.name)
        })
      });


    const capitalizeFirstLetter = (text) => {
        return text.charAt(0).toUpperCase() + text.slice(1)
    }

    const getColumnNamesFromData = (fileContent) => {
        return Object.keys(fileContent[0]).map(key => {
            return ({ name: capitalizeFirstLetter(key), selector: key, sortable: true })
        })
    }
    const [filterText, setFilterText] = useState("");
    const [resetPaginationToggle, setResetPaginationToggle] = useState(false);
    
    const subHeaderComponent = useMemo(() => {
        const handleClear = () => {
        if (filterText) {
        setResetPaginationToggle(!resetPaginationToggle);
        setFilterText("");
        }
    };
    
    return (
        <FilterComponent
        onFilter={e => setFilterText(e.target.value)}
        onClear={handleClear}
        filterText={filterText}
        />
    );
  }, [filterText, resetPaginationToggle]);

    const downloadBeta = (downloadFile)=>{
        download(TSV.stringify(downloadFile), "EntryReportsParsed.tsv", "tsv")
    }


    const checkVoid = (file) =>{
        if(file[0] !== undefined){
            const filteredItems = table[0].fileContent.filter(
                item =>
                  JSON.stringify(item)
                    .toLowerCase()
                    .indexOf(filterText.toLowerCase()) !== -1);
            const download = ()=>{
                downloadBeta(filteredItems)
                }
            return(<div><DataTable
                style={{ width: "100%", height: "100%" , margin: 'auto'}}
                title={file[0].fileName}
                pagination
                paginationRowsPerPageOptions = {[10,20,30,40,50]}
                noHeader
                striped
                subHeader
                subHeaderComponent={subHeaderComponent}
                columns={getColumnNamesFromData(file[0].fileContent)}
                data={filteredItems}
            />
            <Button onClick = {download} variant='contained'
        color='secondary'>
                Click to download the filtered results
            </Button>
            </div>)
        }else{
            return(<div/>)
        }
    }


    return (
        <main className='main'>
            <Toolbar>
                <Typography variant="h6">Entry Reports</Typography>
            </Toolbar>
            {checkVoid(table)}
            
        </main>
    )
}

const EntryReports = ({ outputsFolder }) => {
    return (
        <DashboardLayout>
            <Main style = {{width: "100%", height: "100%"}}
                outputsFolder={outputsFolder}
            />
        </DashboardLayout>
    )
}

export default EntryReports;