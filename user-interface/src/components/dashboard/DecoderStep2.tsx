import * as React from 'react';
import Title from './Title';
import { Button, Grid } from '@mui/material';
import secret from 'assets/images/secret.png';
import X from 'assets/images/X.png';
import X1 from 'assets/images/X1.png';
import X2 from 'assets/images/X2.png';
import imagesZip from 'assets/images/images.zip';

const DecoderStep2 = () => {
    return (
        <React.Fragment>
            <Title>Your crypto message</Title>
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
                        src={X}
                        width="100%"
                        height="auto"
                        alt=""
                    />
                </Grid>
            </Grid>
        </React.Fragment>
    );
};

export default DecoderStep2;