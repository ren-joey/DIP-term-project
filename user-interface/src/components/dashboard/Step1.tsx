import * as React from 'react';
import Title from './Title';
import { TextField, Button } from '@mui/material';

const Step1 = ({
    step,
    setStep
}: {
    step: number,
    setStep: (step: number) => void
}) => {
    return (
        <React.Fragment>
            <Title>Step1: Enter your crypto message</Title>
            <div className="desc">
                Requirements:
                <br />
                1) The maximum number of rows is limited to 2
                <br />
                2) The number of characters should be less than 18
                <br />
            </div>
            <br />
            <TextField
                id="outlined-multiline-static"
                label="Crypto Message"
                multiline
                rows={2}
                value={`NTU_CSIE 臺大資工
●    大資`}
                placeholder="Please enter your crypto message here"
                disabled={step > 1 ? true : false}
            />
            <br />
            <Button
                variant="contained"
                onClick={() => {
                    setStep(2);
                }}
                disabled={step > 1 ? true : false}
            >Enter
            </Button>
        </React.Fragment>
    );
};

export default Step1;