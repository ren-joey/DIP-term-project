import { Container, Grid, Paper } from '@mui/material';
import Step1 from './Step1';
import Step2 from './Step2';
import Step3 from './Step3';
import { useState } from 'react';

const Encoder = () => {
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
                {/* Step1 */}
                <Grid
                    item
                    xs={12}
                >
                    <Paper
                        sx={{
                            p: 2,
                            display: 'flex',
                            flexDirection: 'column'
                        }}
                    >
                        <Step1
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
                                <Step2
                                    step={step}
                                    setStep={setStep}
                                />
                            </Paper>
                        </Grid>
                    )
                }
                {/* Step3 */}
                {
                    step > 2 && (
                        <Grid
                            item
                            xs={12}
                        >
                            <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                                <Step3 />
                            </Paper>
                        </Grid>
                    )
                }
            </Grid>
        </Container>
    );
};

export default Encoder;