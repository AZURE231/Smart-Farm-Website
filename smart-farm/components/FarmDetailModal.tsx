'use client';
import Backdrop from '@mui/material/Backdrop';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import Fade from '@mui/material/Fade';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useState } from 'react';
import { TextField } from '@mui/material';
import { Input } from '@mui/material';
import { TimePicker } from '@mui/x-date-pickers';

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

export default function TransitionsModal({
  open,
  setOpen,
}: {
  open: boolean;
  setOpen: any;
}) {
  const handleClose = () => setOpen(false);

  const checkNumber = (e: any) => {
    if (isNaN(+e.target.value)) {
      alert('Please enter a number');
      e.target.value = '';
    }
  };

  return (
    <div>
      <Modal
        aria-labelledby="transition-modal-title"
        aria-describedby="transition-modal-description"
        open={open}
        onClose={handleClose}
        closeAfterTransition
        slots={{ backdrop: Backdrop }}
        slotProps={{
          backdrop: {
            timeout: 500,
          },
        }}
      >
        <Fade in={open}>
          <Box sx={style}>
            <Typography id="transition-modal-title" variant="h6" component="h2">
              Configuration
            </Typography>
            <form>
              <div className="flex flex-row gap-2">
                <TextField
                  id="mixer_1"
                  label="Mixer 1"
                  variant="outlined"
                  onChange={(e) => {
                    checkNumber(e);
                  }}
                />
                <TextField
                  id="mixer_2"
                  label="Mixer 2"
                  variant="outlined"
                  onChange={(e) => {
                    checkNumber(e);
                  }}
                />
                <TextField
                  id="mixer_3"
                  label="Mixer 3"
                  variant="outlined"
                  onChange={(e) => {
                    checkNumber(e);
                  }}
                />
              </div>
              <div className="mt-3 flex flex-row gap-2">
                <TimePicker label="Start time" />
                <TimePicker label="End time" />
              </div>
              <label className="mr-2">Cycle: </label>
              <Input
                type="number"
                name="Cycle"
                className="w-10"
                onChange={(e) => {
                  if (+e.target.value < 0) {
                    alert('Please enter a positive number');
                    e.target.value = '0';
                  }
                }}
              />
            </form>
            <div className="mt-5">
              <Button onClick={handleClose}>Close</Button>
              <Button type="submit" variant="contained">
                Save
              </Button>
            </div>
          </Box>
        </Fade>
      </Modal>
    </div>
  );
}
