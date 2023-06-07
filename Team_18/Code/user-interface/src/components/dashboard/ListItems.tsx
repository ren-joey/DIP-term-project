import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';
import LockIcon from '@mui/icons-material/Lock';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import AssignmentIcon from '@mui/icons-material/Assignment';

const MainListItems = ({
    setPage
}: {
    setPage: (page: Pages) => void
}) => (
    <React.Fragment>
        <ListItemButton onClick={() => setPage('encode')}>
            <ListItemIcon>
                <LockIcon />
            </ListItemIcon>
            <ListItemText primary="Encode" />
        </ListItemButton>
        <ListItemButton onClick={() => setPage('decode')}>
            <ListItemIcon>
                <LockOpenIcon />
            </ListItemIcon>
            <ListItemText primary="Decode" />
        </ListItemButton>
        {/* <ListItemButton>
            <ListItemIcon>
                <PeopleIcon />
            </ListItemIcon>
            <ListItemText primary="Customers" />
        </ListItemButton>
        <ListItemButton>
            <ListItemIcon>
                <BarChartIcon />
            </ListItemIcon>
            <ListItemText primary="Reports" />
        </ListItemButton>
        <ListItemButton>
            <ListItemIcon>
                <LayersIcon />
            </ListItemIcon>
            <ListItemText primary="Integrations" />
        </ListItemButton> */}
    </React.Fragment>
);

export const secondaryListItems = (
    <React.Fragment>
        <ListSubheader
            component="div"
            inset
        >
            Saved reports
        </ListSubheader>
        <ListItemButton>
            <ListItemIcon>
                <AssignmentIcon />
            </ListItemIcon>
            <ListItemText primary="Current month" />
        </ListItemButton>
        <ListItemButton>
            <ListItemIcon>
                <AssignmentIcon />
            </ListItemIcon>
            <ListItemText primary="Last quarter" />
        </ListItemButton>
        <ListItemButton>
            <ListItemIcon>
                <AssignmentIcon />
            </ListItemIcon>
            <ListItemText primary="Year-end sale" />
        </ListItemButton>
    </React.Fragment>
);

export default MainListItems;