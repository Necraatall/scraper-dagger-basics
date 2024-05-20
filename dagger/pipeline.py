# dagger/pipeline.py
import dagger

async def main():
    config = dagger.Config()

    async with dagger.Connection(config) as client:
        # Define security scan pipeline
        PYTHON_VERSION = "python:3.12"

        security_scan = (
            client.container()
            .from_(PYTHON_VERSION)
            .with_exec(["pip", "install", "trivy"])
            .with_exec([
                "trivy", "fs", "--severity", "HIGH", "--exit-code", "1", "--ignore-unfixed", "."
            ])
        )

        # Define lint pipeline
        lint = (
            client.container()
            .from_(PYTHON_VERSION)
            .with_exec(["pip", "install", "poetry"])
            .with_exec(["poetry", "install"])
            .with_exec(["poetry", "run", "ruff", "src"])
        )

        # Define test pipeline
        test = (
            client.container()
            .from_(PYTHON_VERSION)
            .with_exec(["pip", "install", "poetry"])
            .with_exec(["poetry", "install"])
            .with_exec(["poetry", "run", "pytest", "--cov=src", "tests/"])
        )

        # Run the pipelines
        await security_scan.exit_code()
        await lint.exit_code()
        await test.exit_code()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
