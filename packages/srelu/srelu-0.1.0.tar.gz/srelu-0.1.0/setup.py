from setuptools import setup, find_packages

setup(
    name='srelu',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'tensorflow',
    ],
    author='Siddhanth Bhat',
    author_email='siddhanthbhat@outlook.com',
    description='A library for the SReLU activation function.',
    long_description='The SReLU (Smooth Rectified Linear Unit) is an activation function designed to improve deep learning model performance by providing smooth, differentiable gradients across both positive and negative input domains. Traditional activation functions like ReLU (Rectified Linear Unit) have been widely used for their simplicity and computational efficiency, but they come with some drawbacks, especially when dealing with negative input values, where the gradient becomes zero (leading to the "dying ReLU" problem). SReLU addresses these issues while preserving the benefits of ReLU for positive inputs.',
    long_description_content_type='text/markdown',
    url='https://github.com/SiddhanthBhat/sRELU',  # GitHub repository
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
