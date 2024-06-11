export interface IFarm {
  area: string;
  process: IFarmDetail[];
}

export interface IFarmDetail {
  id: string;
  init_mixer: number[];
  mixer: number[];
  start_time: string;
  end_time: string;
  isActive: boolean;
  isCompleted: boolean;
  cycle: number;
}
