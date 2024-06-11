'use client';
import Backdrop from '@mui/material/Backdrop';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import Fade from '@mui/material/Fade';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { TextField } from '@mui/material';
import { Input } from '@mui/material';
import { TimePicker } from '@mui/x-date-pickers';
import { useState } from 'react';
import { Dayjs } from 'dayjs';
import axios from 'axios';

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
  area,
}: {
  open: boolean;
  setOpen: any;
  area: string;
}) {
  const handleClose = () => setOpen(false);

  const [formData, setFormData] = useState({
    area: area,
    id: '4',
    mixer: ['', '', ''],
    start_time: null as Dayjs | null,
    end_time: null as Dayjs | null,
    cycle: '',
    emergency: false,
  });

  const [responseMessage, setResponseMessage] = useState('');

  const handleMixerChange = (index: number, value: string) => {
    const newMixer = [...formData.mixer];
    newMixer[index] = value;
    setFormData({
      ...formData,
      mixer: newMixer,
    });
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | Dayjs | null,
    field?: string
  ) => {
    if (field) {
      setFormData({
        ...formData,
        [field]: e,
      });
    } else if ('target' in e!) {
      const { name, value } = e.target;
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  const checkNumber = (e: any) => {
    if (isNaN(+e.target.value)) {
      alert('Please enter a number');
      e.target.value = '';
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formattedData = {
      ...formData,
      start_time: formData.start_time
        ? formData.start_time.format('DD/MM/YYYY HH:mm:ss')
        : '',
      end_time: formData.end_time
        ? formData.end_time.format('DD/MM/YYYY HH:mm:ss')
        : '',
    };
    console.log(formattedData);
    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/add_process',
        formattedData
      );
      console.log('Response:', response.data);
    } catch (error) {
      console.error('Error posting data:', error);
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
            <form onSubmit={handleSubmit}>
              <div className="flex flex-row gap-2">
                <TextField
                  id="mixer_1"
                  label="Mixer 1"
                  variant="outlined"
                  name="mixer_1"
                  onChange={(e) => {
                    checkNumber(e);
                    handleMixerChange(0, e.target.value);
                  }}
                />
                <TextField
                  id="mixer_2"
                  label="Mixer 2"
                  variant="outlined"
                  name="mixer_2"
                  onChange={(e) => {
                    checkNumber(e);
                    handleMixerChange(1, e.target.value);
                  }}
                />
                <TextField
                  id="mixer_3"
                  label="Mixer 3"
                  variant="outlined"
                  name="mixer_3"
                  onChange={(e) => {
                    checkNumber(e);
                    handleMixerChange(2, e.target.value);
                  }}
                />
              </div>
              <div className="mt-3 flex flex-row gap-2">
                <TimePicker
                  label="Start time"
                  onChange={(newValue) => handleChange(newValue, 'start_time')}
                />
                <TimePicker
                  label="End time"
                  onChange={(newValue) => handleChange(newValue, 'end_time')}
                />
              </div>
              <label className="mr-2">Cycle: </label>
              <Input
                type="number"
                name="cycle"
                className="w-10"
                onChange={(e) => {
                  if (+e.target.value < 0) {
                    alert('Please enter a positive number');
                    e.target.value = '0';
                  }
                  handleChange(e);
                }}
              />
              <div className="mt-5">
                <Button onClick={handleClose}>Close</Button>
                <Button type="submit" variant="contained">
                  Save
                </Button>
              </div>
            </form>
          </Box>
        </Fade>
      </Modal>
    </div>
  );
}
