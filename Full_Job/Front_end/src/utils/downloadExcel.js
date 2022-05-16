import * as Excel from '@grapecity/spread-excelio';
import { saveAs } from 'file-saver';

function downloadExcel(data, filename) {

    const excelIO = new Excel.IO();

    excelIO.save(data, (blob) => {
        saveAs(blob, filename);
    }, function (e) {
        alert(e);
    });
}

export default downloadExcel;