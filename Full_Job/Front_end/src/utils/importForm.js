import * as React from "react";

export const ImportForm = () => {
  const folderInput= React.useRef(null);

  return (
    <>
       <div className="form-group row">
          <div className="col-lg-6">
            <label>Select Folder</label>
          </div>
          <div className="col-lg-6">
            <input
              type="file"
              directory=""
              webkitdirectory=""
              className="form-control"
              ref={folderInput}
            />
          </div>
        </div>
    </>)
};

export default ImportForm;