import dagger

@dagger.task()
async def create_container():
    async with dagger.Connection() as conn:
        project = conn.project(name="scraper-dagger-basics")

        # Create base container
        container = project.container(
            name="base-container",
            image="python:3.12-slim",
        )

        # Install poetry and dagger
        container.run(
            cmd=["poetry", "install"]
        )
        container.run(
            cmd=["poetry", "run", "python", "-c", 'import os; os.system("curl -L https://dl.dagger.io/dagger/install.sh | DAGGER_VERSION=0.11.4 sudo sh")']
        )
        container.run(
            cmd=["poetry", "add", "dagger-io", "requests"]
        )
        container.run(
            cmd=[
                "sudo", "apt-get", "install", "-y", "wget", "apt-transport-https", "gnupg",
                "&&", "wget", "-qO", "-", "https://aquasecurity.github.io/trivy-repo/deb/public.key",
                "|", "gpg", "--dearmor", "|", "sudo", "tee", "/usr/share/keyrings/trivy.gpg", "> /dev/null",
                "&&", "echo", "'deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main'",
                "|", "sudo", "tee", "/etc/apt/sources.list.d/trivy.list",
                "&&", "sudo", "apt-get", "update",
                "&&", "sudo", "apt-get", "install", "-y", "trivy"
            ]
        )

        return container
