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
  const [activeNextStep, setActiveNextStep] = useState(false)

  const stepComponents = [
    StepName,
    StepAge,
    StepGender,
    StepShowGender,
    StepCity,
    StepHeightWeight,
    StepInterests,
    StepAbout,
    StepSummary,
  ];

  const steps = stepComponents.map((Component) => (
    <Component
      data={data}
      setData={setData}
      setActiveNextStep={setActiveNextStep}
    />
  ));

  const progress = Math.round(((step + 1) / steps.length) * 100);

  return (
    <div className={styles.wrapper}>
      <form className={styles.innerWrapper}>
        <div className={styles.progressBar}>
          <div className={styles.progress}
            style={{ width: `${progress}%` }}
          />
        </div>
        {steps[step]}
        {step > 0 && <button
          onClick={
            () => setStep(step - 1)
          }
          className={styles.formButton}
        >
          Назад
        </button>}
        {step < steps.length - 1
          ? <button
            onClick={(e) => {
              e.preventDefault()
              setStep(step + 1)
            }}
            className={styles.formButton}
            type="submit"
            disabled={!activeNextStep}
          >
            Далее
          </button>
          : <button
            className={styles.formButton}
            type="submit"
          >
            Сохранить
          </button>}
      </form>
    </div>
  );
}
