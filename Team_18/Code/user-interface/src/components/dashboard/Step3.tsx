import * as React from 'react';
import Title from './Title';
import { Button, Grid } from '@mui/material';
// import secret from 'assets/images/secret.png';
import X1 from 'assets/images/X1.png';
import X2 from 'assets/images/X2.png';
import imagesZip from 'assets/images/images.zip';

const Step3 = () => {
    return (
        <React.Fragment>
            <Title>Step3: Download your crypto images</Title>
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
                    <img
                        src={X1}
                        width="100%"
                        height="auto"
                        alt=""
                    />
                </Grid>
                <Grid
                    item
                    xs={12}
                    md={6}
                >
                    <img
                        src={X2}
                        width="100%"
                        height="auto"
                        alt=""
                    />
                </Grid>
            </Grid>
            <br />
            <a
                href={imagesZip}
                style={{
                    display: 'block'
                }}
                download
            >
                <Button
                    variant="contained"
                    fullWidth={true}
                >Download
                </Button>
            </a>
        </React.Fragment>
    );
};

export default Step3;