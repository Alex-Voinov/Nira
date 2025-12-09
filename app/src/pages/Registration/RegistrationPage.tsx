import { useState } from "react";
import StepName from "./steps/StepName";
import StepAge from "./steps/StepAge";
import StepGender from "./steps/StepGender";
import StepShowGender from "./steps/StepShowGender";
import StepCity from "./steps/StepCity";
import StepHeightWeight from "./steps/StepHeightWeight";
import StepInterests from "./steps/StepInterests";
import StepAbout from "./steps/StepAbout";
import StepSummary from "./steps/StepSummary";
import styles from "./RegistrationPage.module.css";
import { formInitialState, type IUser } from "@/types/user";


export default function RegistrationPage() {
  const [step, setStep] = useState(0);

  const [data, setData] = useState<IUser>(formInitialState);


  const steps = [
    <StepName data={data} setData={setData} />,
    <StepAge data={data} setData={setData} />,
    <StepGender data={data} setData={setData} />,
    <StepShowGender data={data} setData={setData} />,
    <StepCity data={data} setData={setData} />,
    <StepHeightWeight data={data} setData={setData} />,
    <StepInterests data={data} setData={setData} />,
    <StepAbout data={data} setData={setData} />,
    <StepSummary data={data} />,
  ];

  const progress = Math.round(((step + 1) / steps.length) * 100);

  return (
    <form className={styles.wrapper}>
      <div className={styles.progressBar}>
        <div className={styles.progress} style={{ width: `${progress}%` }} />
      </div>
      {steps[step]}
      {step > 0 && <button onClick={() => setStep(step - 1)}>
        Назад
      </button>}
      {step < steps.length - 1
        ? <button
          onClick={(e) => {
            e.preventDefault()
            setStep(step + 1)
          }}
          type="submit"
        >
          Далее
        </button>
        : <button
          type="submit"
        >
          Сохранить
        </button>}
    </form>
  );
}
