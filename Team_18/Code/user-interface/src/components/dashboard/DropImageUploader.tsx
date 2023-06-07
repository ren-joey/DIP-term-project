import { useCallback, useMemo, useState } from 'react';
import { useDropzone } from 'react-dropzone';

const baseStyle = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '20px',
    borderWidth: 2,
    borderRadius: 2,
    borderColor: '#eeeeee',
    borderStyle: 'dashed',
    backgroundColor: '#fafafa',
    color: '#bdbdbd',
    outline: 'none',
    transition: 'border .24s ease-in-out'
};

const focusedStyle = {
    borderColor: '#2196f3'
};

const acceptStyle = {
    borderColor: '#00e676'
};

const rejectStyle = {
    borderColor: '#ff1744'
};

const DropImageUploader = () => {
    const [path, setPath] = useState('');
    const onDrop = useCallback(acceptedFiles => {
        setPath(() => {
            const file = acceptedFiles[acceptedFiles.length - 1];
            return URL.createObjectURL(file);
        });
    }, [setPath]);
    const {
        acceptedFiles,
        getRootProps,
        getInputProps,
        isFocused,
        isDragAccept,
        isDragReject
    } = useDropzone({
        onDrop,
        accept: {'image/*': []}
    });
    const style = useMemo(() => ({
        ...baseStyle,
        ...(isFocused ? focusedStyle : {}),
        ...(isDragAccept ? acceptStyle : {}),
        ...(isDragReject ? rejectStyle : {}),
        flexDirection: undefined
    }), [
        isFocused,
        isDragAccept,
        isDragReject
    ]);

    return (
        <div>
            {
                path.length === 0 ? (
                    <div {...getRootProps({style})}>
                        <input {...getInputProps()} />
                        <p style={{textAlign: 'center', width: '100%'}}>
                            <br />
                            Drag and drop your image here
                            <br />
                            <br />
                        </p>
                    </div>
                ) : (
                    <img
                        src={path}
                        width="100%"
                        height="auto"
                        alt={acceptedFiles[acceptedFiles.length - 1].name}
                    />
                )
            }
        </div>
    );
};

export default DropImageUploader;