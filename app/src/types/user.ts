export type IUser = {
  tg_id: number;
  name: string;
  birthDate: string;
  gender: "male" | "female" | "other" | null;
  show_gender: "male" | "female" | "mix" | null;
  city: string;
  current_country: string;
  height: number | null;
  weight: number | null;
  goal: string[];
  description: string | null;
};

export const formInitialState: IUser = {
  name: "",
  birthDate: '',
  gender: null,
  show_gender: null,
  city: "",
  current_country: 'UK',
  height: null,
  weight: null,
  goal: [],
  description: "",
  tg_id: -1,
};