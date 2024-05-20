# # dagger/pipeline.py
# import dagger

# async def main():
#     config = dagger.Config()

#     async with dagger.Connection(config) as client:
#         # Define security scan pipeline
#         PYTHON_VERSION = "python:3.12"

#         security_scan = (
#             client.container()
#             .from_(PYTHON_VERSION)
#             .with_exec(["pip", "install", "trivy"])
#             .with_exec([
#                 "trivy", "fs", "--severity", "HIGH", "--exit-code", "1", "--ignore-unfixed", "."
#             ])
#         )

#         # Define lint pipeline
#         lint = (
#             client.container()
#             .from_(PYTHON_VERSION)
#             .with_exec(["pip", "install", "poetry"])
#             .with_exec(["poetry", "install"])
#             .with_exec(["poetry", "run", "ruff", "src"])
#         )

#         # Define test pipeline
#         test = (
#             client.container()
#             .from_(PYTHON_VERSION)
#             .with_exec(["pip", "install", "poetry"])
#             .with_exec(["poetry", "install"])
#             .with_exec(["poetry", "run", "pytest", "--cov=src", "tests/"])
#         )

#         # Run the pipelines
#         await security_scan.exit_code()
#         await lint.exit_code()
#         await test.exit_code()

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())

# dagger/pipeline.py
# #### verze 2
# import dagger

# async def main():
#     async with dagger.Connection() as conn:
#         project = conn.project(name="stock-scraper")

#         # Lint pipeline
#         lint = project.pipeline("lint")
#         lint.task("run lint", cmd=["poetry", "run", "ruff", "src"])

#         # Test pipeline
#         test = project.pipeline("test")
#         test.task("run tests", cmd=["poetry", "run", "pytest"])

#         # Security scan pipeline
#         security_scan = project.pipeline("security_scan")
#         security_scan.task("run trivy scan", cmd=["trivy", "fs", "--exit-code", "1", "--severity", "HIGH,CRITICAL", "--ignore-unfixed", "."])

#         # Fix vulnerabilities pipeline
#         fix_vulnerabilities = project.pipeline("fix_vulnerabilities")
#         fix_vulnerabilities.task("run trivy fix", cmd=["trivy", "fs", "--exit-code", "0", "--severity", "HIGH,CRITICAL", "--ignore-unfixed", "--fix", "."])

#         await lint.run()
#         await test.run()
#         await security_scan.run()
#         await fix_vulnerabilities.run()

# if __name__ == "__main__":
#     dagger.run(main)


# dagger/pipeline.py
# ########verze 3
# import dagger
# import os

# async def main():
#     async with dagger.Connection() as conn:
#         project = conn.project(name="stock-scraper")

#         # Task: Install dependencies
#         install_dependencies = project.pipeline("install_dependencies")
#         install_dependencies.task(
#             "install poetry dependencies",
#             cmd=["poetry", "install"]
#         )
#         install_dependencies.task(
#             "install dagger",
#             cmd=["poetry", "run", "python", "-c", 'import os; os.system("curl -L https://dl.dagger.io/dagger/install.sh | DAGGER_VERSION=0.11.4 sudo sh")']
#         )
#         install_dependencies.task(
#             "add dependencies",
#             cmd=["poetry", "add", "dagger-io", "requests"]
#         )
#         install_dependencies.task(
#             "install system dependencies",
#             cmd=[
#                 "sudo", "apt-get", "install", "-y", "wget", "apt-transport-https", "gnupg",
#                 "&&", "wget", "-qO", "-", "https://aquasecurity.github.io/trivy-repo/deb/public.key",
#                 "|", "gpg", "--dearmor", "|", "sudo", "tee", "/usr/share/keyrings/trivy.gpg", "> /dev/null",
#                 "&&", "echo", "'deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main'",
#                 "|", "sudo", "tee", "/etc/apt/sources.list.d/trivy.list",
#                 "&&", "sudo", "apt-get", "update",
#                 "&&", "sudo", "apt-get", "install", "-y", "trivy"
#             ]
#         )

#         # Task: Run linting
#         lint = project.pipeline("lint")
#         lint.task(
#             "run lint",
#             cmd=["poetry", "run", "ruff", "src"]
#         )

#         # Task: Run tests with coverage
#         test = project.pipeline("test")
#         test.task(
#             "run tests",
#             cmd=["poetry", "run", "pytest", "--cov=src", "tests/"]
#         )

#         # Task: Run security scan
#         security_scan = project.pipeline("security_scan")
#         security_scan.task(
#             "run trivy scan",
#             cmd=[
#                 "trivy", "fs", "--exit-code", "1",
#                 "--severity", "HIGH,CRITICAL", "--ignore-unfixed", "."
#             ]
#         )

#         # Task: Fix vulnerabilities
#         fix_vulnerabilities = project.pipeline("fix_vulnerabilities")
#         fix_vulnerabilities.task(
#             "run trivy fix",
#             cmd=[
#                 "trivy", "fs", "--exit-code", "0",
#                 "--severity", "HIGH,CRITICAL", "--ignore-unfixed", "--fix", "."
#             ]
#         )

#         # Run all tasks in sequence
#         await install_dependencies.run()
#         await lint.run()
#         await test.run()
#         await security_scan.run()
#         await fix_vulnerabilities.run()

# if __name__ == "__main__":
#     dagger.run(main)


# # dagger/pipeline.py
# #### verze 4 rozdeleni base a pipeline
# import dagger
# from ..container.container_base import create_container

# @dagger.task()
# async def main():
#     async with dagger.Connection() as conn:
#         project = conn.project(name="scraper-dagger-basics")

#         # Získání základního kontejneru
#         container = await create_container()

#         # Lint pipeline
#         lint = project.pipeline("lint")
#         lint.task(
#             "run lint",
#             cmd=["poetry", "run", "ruff", "src"]
#         )

#         # Test pipeline
#         test = project.pipeline("test")
#         test.task(
#             "run tests",
#             cmd=["poetry", "run", "pytest", "--cov=src", "tests/"]
#         )

#         # Security scan pipeline
#         security_scan = project.pipeline("security_scan")
#         security_scan.task(
#             "run trivy scan",
#             cmd=[
#                 "trivy", "fs", "--exit-code", "1",
#                 "--severity", "HIGH,CRITICAL", "--ignore-unfixed", "."
#             ]
#         )

#         # Fix vulnerabilities pipeline
#         fix_vulnerabilities = project.pipeline("fix_vulnerabilities")
#         fix_vulnerabilities.task(
#             "run trivy fix",
#             cmd=[
#                 "trivy", "fs", "--exit-code", "0",
#                 "--severity", "HIGH,CRITICAL", "--ignore-unfixed", "--fix", "."
#             ]
#         )

#         # Run all tasks in sequence
#         await lint.run(container)
#         await test.run(container)
#         await security_scan.run(container)
#         await fix_vulnerabilities.run(container)

# ### verze 5 pokus o pipelines bez yaml
# # pipelines.py

# import dagger
# from container.container_base import create_container

# @dagger.task()
# async def lint_pipeline(container):
#     # Definice úloh pro linting pipeline
#     print("Running lint pipeline...")
#     # Zde přidej kód pro linting pipeline
#     await container.run(cmd=["poetry", "run", "ruff", "src"])

# @dagger.task()
# async def test_pipeline(container):
#     # Definice úloh pro testovací pipeline
#     print("Running test pipeline...")
#     # Zde přidej kód pro testovací pipeline
#     await container.run(cmd=["poetry", "run", "pytest", "--cov=src", "tests/"])

# @dagger.task()
# async def security_scan_pipeline(container):
#     # Definice úloh pro bezpečnostní skenovací pipeline
#     print("Running security scan pipeline...")
#     # Zde přidej kód pro bezpečnostní skenovací pipeline
#     await container.run(cmd=["trivy", "fs", "--exit-code", "1", "--severity", "HIGH,CRITICAL", "--ignore-unfixed", "."])

# @dagger.task()
# async def fix_vulnerabilities_pipeline(container):
#     print("Running fix vulnerabilities pipeline...")
#     await container.run(cmd=["trivy", "fs", "--exit-code", "0", "--severity", "HIGH,CRITICAL", "--ignore-unfixed", "--fix", "."])

# if __name__ == "__main__":
#     # Získání základního kontejneru
#     container = await create_container()

#     # Spuštění jednotlivých pipelin
#     await lint_pipeline(container)
#     await test_pipeline(container)
#     await security_scan_pipeline(container)
#     await fix_vulnerabilities_pipeline(container)

### verze 6 pokus o pipeline bez yaml II
# pipelines.py
import dagger

@dagger.task()
async def checkout_code(container):
    return container.use("actions/checkout@v2")

@dagger.task()
async def setup_python(container):
    return container.use("setup-python@v2", inputs={"python-version": "3.x"})

@dagger.task()
async def install_dependencies(container):
    await container.run(cmd=["python", "-m", "pip", "install", "--upgrade", "pip"])
    await container.run(cmd=["pip", "install", "poetry"])
    return await container.run(cmd=["poetry", "install"])

@dagger.task()
async def run_linting(container):
    await container.run(cmd=["poetry", "run", "ruff", "src"])

@dagger.task()
async def run_tests(container):
    await container.run(cmd=["poetry", "run", "pytest", "--cov=src", "tests/"])

@dagger.task()
async def run_security_scan(container):
    await container.run(cmd=["trivy", "fs", "--exit-code", "1", "--severity", "HIGH,CRITICAL", "--ignore-unfixed", "."])

@dagger.task()
async def fix_vulnerabilities_pipeline(container):
    print("Running fix vulnerabilities pipeline...")
    await container.run(cmd=["trivy", "fs", "--exit-code", "0", "--severity", "HIGH,CRITICAL", "--ignore-unfixed", "--fix", "."])

@dagger.pipeline(name="lint_pipeline")
async def lint_pipeline():
    container = await checkout_code(dagger.Container())
    container = await setup_python(container)
    container = await install_dependencies(container)
    await run_linting(container)

@dagger.pipeline(name="test_pipeline")
async def test_pipeline():
    container = await checkout_code(dagger.Container())
    container = await setup_python(container)
    container = await install_dependencies(container)
    await run_tests(container)

@dagger.pipeline(name="security_scan_pipeline")
async def security_scan_pipeline():
    container = await checkout_code(dagger.Container())
    container = await setup_python(container)
    container = await install_dependencies(container)
    await run_security_scan(container)

@dagger.pipeline(name="fix_vulnerabilities_pipeline")
async def fix_vulnerabilities():
    container = await checkout_code(dagger.Container())
    container = await setup_python(container)
    container = await install_dependencies(container)
    await fix_vulnerabilities_pipeline(container)
