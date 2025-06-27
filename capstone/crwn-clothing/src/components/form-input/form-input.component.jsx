import '../form-input/form-input.styles.scss';

const FormInput = ({ label, ...otherProps }) => {
    return(
        <div className="group">
            <input {...otherProps} className="form-input" />
            {
                label &&
                <label className={`${otherProps.value ? 'shrink' : ''} form-input-label`}>{label}</label>
            }
        </div>
    );
}

export default FormInput