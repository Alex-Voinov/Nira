import type { FC } from "react";
import type { IStep } from "../RegistrationPage";
import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const StepAge: FC<IStep> = ({ data, setData }) => {
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());

  const handleChange = (date: Date | null) => {
    setSelectedDate(date);
    setData({
      ...data,
      birthDate: date ? date.toISOString().split("T")[0] : "",
    });
  };

  return (
    <div className="step">
      <h2>Дата рождения</h2>
      <DatePicker
        selected={selectedDate}
        onChange={handleChange}
        maxDate={new Date()}
        dateFormat="yyyy-MM-dd"
        placeholderText="Выберите дату"
        showMonthDropdown
        showYearDropdown
        dropdownMode="select"
      />
    </div>
  );
};

export default StepAge;
