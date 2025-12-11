import type { FC } from "react";
import type { IStep } from "../RegistrationPage";

const StepSummary: FC<IStep> = ({ data }) => {
    return (
        <div className="step">
            <h2>Проверь свои данные</h2>
            <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
    );
}

export default StepSummary
