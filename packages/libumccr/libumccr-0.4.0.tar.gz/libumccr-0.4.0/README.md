# libumccr

[![Pull Request Build Status](https://github.com/umccr/libumccr/workflows/Pull%20Request%20Build/badge.svg)](https://github.com/umccr/libumccr/actions) [![PyPI - Downloads](https://img.shields.io/pypi/dm/libumccr?style=flat)](https://pypistats.org/packages/libumccr) [![PyPI](https://img.shields.io/pypi/v/libumccr?style=flat)](https://pypi.org/project/libumccr) 
[![PyPI - License](https://img.shields.io/pypi/l/libumccr?style=flat)](https://opensource.org/licenses/MIT)

UMCCR Reusable Python modules

## Usage

- Install through ``pip`` like so
```
pip install libumccr[aws]
```

- Somewhere in your Python code
```python
from libumccr.aws import libssm

ssm_value = libssm.get_ssm_param("my_param_name")
```

- Crawling S3 Objects from a Bucket, efficiently!
```python
from libumccr.aws import libs3

bucket="my-bucket"
key_prefix="my_prefix"
key_suffix=".csv"

for obj in libs3.get_matching_s3_objects(bucket, prefix=key_prefix, suffix=key_suffix):
    print(f"s3://{bucket}/{obj['Key']}")
```

## Transitive Dependencies

### Self Service

- Starting from `v0.4` onwards, by default, the libumccr does not mandate any transitive dependencies installation for you.
- That is, if you `pip install libumccr` then it just installs the libumccr package itself only. 
- If you do this, you will have to manage transitive dependencies at your application as _end-of-chain_ requirement as you see fit. 
- This depends on which libumccr modules you need to depend on at your code.
- The _bare metal_ libumccr should only have some hundred KB (~180KB) by size. However, in this case, you can only use those modules that leverage built-in Python standard library (that does not require extra 3rd party library). Which might be perfect for use case like [libregex](libumccr/libregex.py) - well-known sample ID pattern parser contributed by team member ([Alexis](https://github.com/alexiswl)). You may contribute here similar and, reuse it at your end...

### Feature Flag

- If you would like to have all transitive dependencies requirement along with the libumccr, then do so `pip install libumccr[all]`.
- For any aws related module usage with boto3 and botocore, then `pip install libumccr[aws]`.
- Similarly, for gspread, gdrive and Pandas dataframe stuff, then `pip install libumccr[libgdrive]`.
- Do check out [setup.py](setup.py) `extras_require` sections for all available feature flags. 

_This arrangement is sometime also known as deferring feature flag toggle at runtime requirement. Google for more..._

### AWS Lambda

- The AWS Lambda runtime for Python environment already contain the boto3 and botocore.
- Hence, if you are bundling your application for AWS Lambda Python runtime environment then you just need to `pip install libumccr`. 
- The AWS Lambda Python runtime is already satisfied the `libumccr[aws]` feature requirement, and you can still leverage the [libumccr.aws](libumccr/aws) modules with the lowest asset bundle footprint. 
- In this case, you just put `boto3` in your local development environment only; such as `reqirements-dev.txt` or equivalent.

## Development

- Create Python virtual environment
```
git clone https://github.com/umccr/libumccr.git
cd libumccr
conda activate libumccr
make install all
make check
make test
```
