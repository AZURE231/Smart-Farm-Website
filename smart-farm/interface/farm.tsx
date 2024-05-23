export interface IFarm {
  id: string;
  name: string;
  description: string;
  image: string;
  details?: IFarmDetail;
}

export interface IFarmDetail {
  id: string;
  mixer_1: string;
  mixer_2: string;
  mixer_3: string;
  start_time: string;
  end_time: string;
  date: string;
  isActivated: boolean;
  cycle: number;
}
