import { Container, Grid, Paper } from '@mui/material';
import Step1 from './Step1';
import Step2 from './Step2';
import Step3 from './Step3';
import { useState } from 'react';
import DecoderStep1 from './DecoderStep1';
import DecoderStep2 from './DecoderStep2';

const Decoder = () => {
    const [step, setStep] = useState(1);

    return (
        <Container
            maxWidth="lg"
            sx={{ mt: 4, mb: 4 }}
        >
            <Grid
                container
                spacing={3}
            >
                <Grid
                    item
                    xs={12}
                >
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <DecoderStep1
                            step={step}
                            setStep={setStep}
                        />
                    </Paper>
                </Grid>
                {/* Step2 */}
                {
                    step > 1 && (
                        <Grid
                            item
                            xs={12}
                        >
                            <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                                <DecoderStep2 />
                            </Paper>
                        </Grid>
                    )
                }
            </Grid>
        </Container>
    );
};

export default Decoder;