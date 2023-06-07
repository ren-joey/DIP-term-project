import * as React from 'react';
// import { useMemo, useCallback, useState } from 'react';
import Title from './Title';
import { Button, Grid } from '@mui/material';
// import { useDropzone } from 'react-dropzone';
import DropImageUploader from './DropImageUploader';



const Step2 = ({
    step,
    setStep
}: {
    step: number,
    setStep: (step: number) => void
}) => {
    return (
        <React.Fragment>
            <Title>Step2: Upload 2 grayscale images</Title>
            <div className="desc">
                Requirements:
                <br />
                1) These 2 images should have the same size
                <br />
                2) The width and height of images should be less than 150 pixel
                <br />
            </div>
            <br />
            <Grid
                container
                spacing={3}
            >
                <Grid
                    item
                    xs={12}
                    md={6}
                >
                    <DropImageUploader />
                </Grid>
                <Grid
                    item
                    xs={12}
                    md={6}
                >
                    <DropImageUploader />
                </Grid>
            </Grid>
            <br />
            <Button
                variant="contained"
                onClick={() => {
                    setStep(3);
                }}
                disabled={step > 2 ? true : false}
            >Uploads
            </Button>
        </React.Fragment>
    );
};

export default Step2;