import React, { useEffect, useState } from 'react';
import DropZone from '../dropzone/dropzone'
import Sidebar from '../sidebar/sidebar';
import "./home.css"

function Home() {
  const [file, setFile] = useState<FileReader>();

  useEffect(() => {
    console.log(file);
  }, [file]);

  return (
    <div className='d-flex'>
      <div>
        <Sidebar />
      </div>
        {!file && 
            <div className='header'>
                <DropZone {...{setFile: setFile}}/>
            </div>
        }

    </div>
  );
}

export default Home;
