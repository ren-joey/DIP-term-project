import * as React from 'react';
import { useMemo, useCallback, useState } from 'react';
import Title from './Title';
import { TextField, Button, Container, Grid } from '@mui/material';
import { useDropzone } from 'react-dropzone';
import DropImageUploader from './DropImageUploader';



const DecoderStep1 = ({
    step,
    setStep
}: {
    step: number,
    setStep: (step: number) => void
}) => {
    return (
        <React.Fragment>
            <Title>Upload 2 crypto images</Title>
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
                    setStep(2);
                }}
                disabled={step > 1 ? true : false}
            >Uploads
            </Button>
        </React.Fragment>
    );
};

export default DecoderStep1;