# DevOps MCP Servers

A curated list of awesome MCP servers focused on DevOps tools and capabilities.

Curated by **[rohitg00/awesome-devops-mcp-servers](https://github.com/rohitg00/awesome-devops-mcp-servers)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

225 entries · 215 distinct repos · 27 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/awslabs/mcp"><img src="https://raw.githubusercontent.com/awslabs/mcp/main/docs/images/root-readme/install-cline-extension.png" width="260"></a> | <a href="https://github.com/cloudflare/mcp-server-cloudflare"><img src="https://github.com/user-attachments/assets/872e253f-23ce-43b3-983c-45f9d0f66100" width="260"></a> | <a href="https://github.com/containers/kubernetes-mcp-server"><img src="https://raw.githubusercontent.com/manusa/kubernetes-mcp-server/main/docs/images/vibe-coding.jpg" width="260"></a> |
| **[awslabs/mcp](https://github.com/awslabs/mcp)**<br>★ 9.7k | **[cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare)**<br>★ 4.3k | **[manusa/kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server)**<br>★ 2.1k |
| <a href="https://github.com/Flux159/mcp-server-kubernetes"><img src="https://opengraph.githubassets.com/1/Flux159/mcp-server-kubernetes" width="260"></a> | <a href="https://github.com/rohitg00/kubectl-mcp-server"><img src="https://github.com/user-attachments/assets/616b4e65-37bc-474e-8124-68e64c6d7c95" width="260"></a> | <a href="https://github.com/weibaohui/k8m"><img src="https://github.com/user-attachments/assets/0951d6c1-389c-49cb-b247-84de15b6ec0e" width="260"></a> |
| **[Flux159/mcp-server-kubernetes](https://github.com/Flux159/mcp-server-kubernetes)**<br>★ 1.6k | **[rohitg00/kubectl-mcp-server](https://github.com/rohitg00/kubectl-mcp-server)**<br>★ 960 | **[weibaohui/k8m](https://github.com/weibaohui/k8m)**<br>★ 885 |

## Contents

- [Cloud Providers](#cloud-providers) (17)
- [Container Orchestration](#container-orchestration) (15)
- [Infrastructure as Code](#infrastructure-as-code) (9)
- [Database Management](#database-management) (1)
- [Version Control](#version-control) (10)
- [Command Line](#command-line) (12)
- [Security](#security) (37)
- [Testing &amp; Chaos Engineering](#testing--chaos-engineering) (6)
- [Code Execution](#code-execution) (4)
- [Dependency Analysis](#dependency-analysis) (5)
- [Continuous Integration](#continuous-integration) (4)
- [DevOps Visibility](#devops-visibility) (3)
- [Mobile CI/CD](#mobile-cicd) (1)
- [Browser Automation](#browser-automation) (20)
- [Coding Agents](#coding-agents) (14)
- [Aggregators](#aggregators) (24)
- [Frameworks](#frameworks) (4)
- [Metrics &amp; Monitoring](#metrics--monitoring) (6)
- [Application Performance Monitoring](#application-performance-monitoring) (13)
- [Alerting &amp; Notification](#alerting--notification) (1)
- [Social Media Monitoring](#social-media-monitoring) (1)
- [Related Resources](#related-resources) (3)
- [Memory &amp; Context](#memory--context) (8)
- [Project Management](#project-management) (3)
- [Ticketing Systems](#ticketing-systems) (2)
- [CMS &amp; Web Platforms](#cms--web-platforms) (1)
- [API Cost Management](#api-cost-management) (1)

## Cloud Providers

- **[awslabs/mcp](https://github.com/awslabs/mcp)** — Official AWS MCP server for interacting with AWS services using the Model Context Protocol. Enables AI assistants to manage AWS resources through natural language and programmatic interfaces
  <sub>★ 9.7k · Python · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/awslabs/mcp.git`</sub>
- **[cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare)** — Integration with Cloudflare services including Workers, KV, R2, and D1
  <sub>★ 4.3k · TypeScript · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cloudflare/mcp-server-cloudflare.git`</sub>
- **[Tiberriver256/mcp-server-azure-devops](https://github.com/Tiberriver256/mcp-server-azure-devops)** — Azure DevOps integration for repository management, work items, and pipelines
  <sub>★ 392 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @tiberriver256/mcp-server-azure-devops`</sub>
- **[eniayomi/gcp-mcp](https://github.com/eniayomi/gcp-mcp)** — A Model Context Protocol server for Google Cloud Platform, enabling AI assistants to interact with GCP resources
  <sub>★ 200 · TypeScript · MIT · clone · pushed 2025-05-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/eniayomi/gcp-mcp`</sub>
- **[alexei-led/aws-mcp-server](https://github.com/alexei-led/cloud-mcp-server)** — A lightweight but powerful server that enables AI assistants to execute AWS CLI commands, use Unix pipes, and apply prompt templates for common AWS tasks in a safe Docker environment with multi-architecture support
  <sub>★ 186 · Python · MIT · source · pushed 2026-02-27 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/alexei-led/aws-mcp-server.git`</sub>
- **[aliyun/alibaba-cloud-ops-mcp-server](https://github.com/aliyun/alibaba-cloud-ops-mcp-server)** — A MCP server that enables AI assistants to operation resources on Alibaba Cloud, supporting ECS, Cloud Monitor, OOS and widely used cloud products
  <sub>★ 130 · Python · Apache-2.0 · source · pushed 2026-03-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aliyun/alibaba-cloud-ops-mcp-server.git`</sub>
- **[Vortiago/mcp-azure-devops](https://github.com/Vortiago/mcp-azure-devops)** — A Model Context Protocol server enabling AI assistants to interact with Azure DevOps services via Python SDK
  <sub>★ 79 · Python · MIT · pip · pushed 2025-10-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-azure-devops`</sub>
- **[bright8192/esxi-mcp-server](https://github.com/bright8192/esxi-mcp-server)** — A VMware ESXi/vCenter management server based on MCP (Model Control Protocol), providing simple REST API interfaces for virtual machine management
  <sub>★ 64 · Python · MIT · source · pushed 2025-07-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/bright8192/esxi-mcp-server.git`</sub>
- **[stefanskiasan/azure-devops-mcp-server](https://github.com/stefanskiasan/azure-devops-mcp-server)** — MCP Server for Cline to Access Azure DevOps
  <sub>★ 33 · TypeScript · MIT · npx · pushed 2025-02-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @stefanskiasan/azure-devops-mcp-server --client claude`</sub>
- **[hardik-id/azure-resource-graph-mcp-server](https://github.com/hardik-id/azure-resource-graph-mcp-server)** — /🏠 - A Model Context Protocol server for querying and analyzing Azure resources at scale using Azure Resource Graph, enabling AI assistants to explore and monitor Azure infrastructure
  <sub>★ 18 · TypeScript · MIT · source · pushed 2025-05-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hardik-id/azure-resource-graph-mcp-server.git`</sub>
- **[aaronsb/ado-mcp](https://github.com/aaronsb/ado-mcp)** — Azure DevOps MCP Server for integrating AI assistants with Azure DevOps services
  <sub>★ 17 · TypeScript · MIT · source · pushed 2025-03-24 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/aaronsb/ado-mcp.git`</sub>
- **[thunderboltsid/mcp-nutanix](https://github.com/thunderboltsid/mcp-nutanix)** — /☁️ - Go-based MCP Server for interfacing with Nutanix Prism Central resources
  <sub>★ 13 · Go · MIT · clone · pushed 2026-01-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/thunderboltsid/mcp-nutanix.git`</sub>
- **[erikhoward/adls-mcp-server](https://github.com/erikhoward/adls-mcp-server)** — /🏠 - MCP Server for Azure Data Lake Storage. It can perform manage containers, read/write/upload/download operations on container files and manage file metadata
  <sub>★ 6 · Python · MIT · clone · pushed 2025-05-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/erikhoward/adls2-mcp-server.git`</sub>
- **[Chain.Love MCP](https://github.com/Chain-Love/chain.love-mcp)** — Hosted MCP gateway for discovering and comparing Web3 infrastructure services such as RPCs, indexing, oracles, storage, compute, and developer tools
  <sub>★ 2 · source · pushed 2026-04-16</sub>
  <sub>`git clone https://github.com/Chain-Love/chain.love-mcp.git`</sub>
- **[arnstarn/mcp-server-spotinst](https://github.com/arnstarn/mcp-server-spotinst)** — MCP server for Spot.io (Spotinst) API with 23 tools for managing Ocean clusters, VNGs, Elastigroups, costs, right-sizing, and logs across AWS and Azure with multi-account support
  <sub>★ 1 · Python · MIT · uv · pushed 2026-05-05 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx mcp-server-spotinst`</sub>
- **[jdubois/azure-cli-mcp](https://github.com/jdubois/azure-cli-mcp)** — A wrapper around the Azure CLI command line that allows you to talk directly to Azure
  <sub>unavailable</sub>
- **[Qovery/qovery-mcp-server](https://mcp.qovery.com/mcp)** — Enterprise Kubernetes management via MCP. Deploy and manage applications, databases, Helm charts, and Terraform modules on AWS EKS, GCP GKE, Azure AKS, and Scaleway. Query environments, troubleshoot deployments, monitor infrastructure. Docs. Also has an AI Agent Skill for deploying from Claude Code, Cursor, and 30+ tools
  <sub>website</sub>
  <sub>`https://mcp.qovery.com/mcp`</sub>

## Container Orchestration

- **[manusa/kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server)** — A powerful Kubernetes MCP server with additional support for OpenShift. Besides providing CRUD operations for any Kubernetes resource, this server provides specialized tools to interact with your cluster
  <sub>★ 2.1k · Go · Apache-2.0 · npx · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx kubernetes-mcp-server@latest --help`</sub>
- **[Flux159/mcp-server-kubernetes](https://github.com/Flux159/mcp-server-kubernetes)** — /🏠 - Typescript implementation of Kubernetes cluster operations for pods, deployments, services
  <sub>★ 1.6k · TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx mcp-chat --server "npx mcp-server-kubernetes"`</sub>
- **[rohitg00/kubectl-mcp-server](https://github.com/rohitg00/kubectl-mcp-server)** — /🏠 - A Model Context Protocol (MCP) server for Kubernetes that enables AI assistants like Claude, Cursor, and others to interact with Kubernetes clusters through natural language
  <sub>★ 960 · Python · MIT · npm · pushed 2026-04-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g kubectl-mcp-server`</sub>
- **[weibaohui/k8m](https://github.com/weibaohui/k8m)** — /🏠 - Provides MCP multi-cluster Kubernetes management and operations, featuring a management interface, logging, and nearly 50 built-in tools covering common DevOps and development scenarios. Supports both standard and CRD resources
  <sub>★ 885 · Go · MIT · source · pushed 2026-09-12 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/weibaohui/k8m.git`</sub>
- **[strowk/mcp-k8s-go](https://github.com/strowk/mcp-k8s-go)** — /🏠 - Kubernetes cluster operations through MCP
  <sub>★ 384 · Go · MIT · npm · pushed 2025-12-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g @strowk/mcp-k8s`</sub>
- **[Higangssh/homebutler](https://github.com/Higangssh/homebutler)** — All-in-one homelab management MCP server for Docker container monitoring, volume backup/restore (including compose and env files), Wake-on-LAN, network scanning, and multi-server management via SSH. Single Go binary with zero dependencies
  <sub>★ 289 · Go · MIT · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g homebutler`</sub>
- **[portainer/portainer-mcp](https://github.com/portainer/portainer-mcp)** — /🏠 - A powerful MCP server that enables AI assistants to seamlessly interact with Portainer instances, providing natural language access to container management, deployment operations, and infrastructure monitoring capabilities
  <sub>★ 233 · Python · MIT · docker · pushed 2026-09-19 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`docker run -d --name portainer-mcp -p 17717:17717 \`</sub>
- **[alexei-led/k8s-mcp-server](https://github.com/alexei-led/k8s-mcp-server)** — A lightweight yet robust server that empowers AI assistants to securely execute Kubernetes CLI commands (kubectl, helm, istioctl, and argocd) using Unix pipes in a safe Docker environment with multi-architecture support
  <sub>★ 212 · Python · MIT · source · pushed 2026-02-27 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/alexei-led/k8s-mcp-server.git`</sub>
- **[weibaohui/kom](https://github.com/weibaohui/kom)** — /🏠 - Provides MCP multi-cluster Kubernetes management and operations. It can be integrated as an SDK into your own project and includes nearly 50 built-in tools covering common DevOps and development scenarios. Supports both standard and CRD resources
  <sub>★ 149 · Go · MIT · source · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/weibaohui/kom.git`</sub>
- **[kubestellar/console (kc-agent)](https://github.com/kubestellar/console)** — (docs) 🏎️ 🏠 - MCP server bridging AI assistants to Kubernetes clusters via kubeconfig. Supports multi-cluster operations, natural language kubectl commands, and integrates with 20+ CNCF tools. CNCF Sandbox project
  <sub>★ 137 · TypeScript · Apache-2.0 · script · pushed 2026-09-21 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/kubestellar/console/main/start.sh | bash`</sub>
- **[kocierik/mcp-nomad](https://github.com/kocierik/mcp-nomad)** — /🏠 - MCP Server for nomad management, and analyze your cluster, application health, logs and ACL
  <sub>★ 59 · Go · MIT · npm · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @kocierik/mcp-nomad`</sub>
- **[wenhuwang/mcp-k8s-eye](https://github.com/wenhuwang/mcp-k8s-eye)** — /🏠 - MCP Server for kubernetes management, and analyze your cluster, application health
  <sub>★ 29 · Go · Apache-2.0 · clone · pushed 2025-05-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wenhuwang/mcp-k8s-eye.git`</sub>
- **[rrmistry/tilt-mcp](https://github.com/rrmistry/tilt-mcp)** — Model Context Protocol server that integrates with Tilt to provide programmatic access to Tilt resources, logs, and management operations for Kubernetes development environments
  <sub>★ 6 · Python · MIT · pip · pushed 2026-03-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install tilt-mcp`</sub>
- **[aadarshjain/kubectl-mcp-server](https://github.com/aadarshjain/kubectl-mcp-server)** — A STDIO based MCP server for Kubernetes that interacts seamlessly with your local clusters (~/.kube/config) using kubectl CLI commands. Uses read-only operations by default to prevent accidental modifications/deletion of K8s resources
  <sub>★ 2 · Python · MIT · source · pushed 2025-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aadarshjain/kubectl-mcp-server.git`</sub>
- **[rog0x/mcp-docker-tools](https://github.com/rog0x/mcp-docker-tools)** — Container management, image analysis, Dockerfile generation, compose validation, and resource monitoring
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-03-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/rog0x/mcp-docker-tools.git`</sub>

## Infrastructure as Code

- **[nwiizo/tfmcp](https://github.com/nwiizo/tfmcp)** — A Terraform MCP server allowing AI assistants to manage and operate Terraform environments, enabling reading configurations, analyzing plans, applying configurations, and managing Terraform state
  <sub>★ 371 · Rust · MIT · cargo · pushed 2026-09-17 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`cargo install tfmcp --version 0.2.3`</sub>
- **[severity1/terraform-cloud-mcp](https://github.com/severity1/terraform-cloud-mcp)** — A Model Context Protocol server that integrates AI assistants with the Terraform Cloud API, allowing you to manage your infrastructure
  <sub>★ 23 · Python · MIT · clone · pushed 2025-11-02 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/severity1/terraform-cloud-mcp.git`</sub>
- **[stakpak/mcp](https://github.com/stakpak/mcp)** — MCP Server for interacting, editing and generating code for Terraform, Kubernetes, GithubActions and Dockerfile
  <sub>★ 18 · JavaScript · Apache-2.0 · npx · pushed 2026-07-04 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @stakpak/mcp STAKPAK_API_KEY=<your-stakpak-api-key>`</sub>
- **[jashkahar/Terraform-MCP-Server](https://github.com/jashkahar/Terraform-MCP-Server)** — This project provides an MCP server that exposes Terraform infrastructure-as-code operations through natural language
  <sub>★ 3 · Python · clone · pushed 2025-03-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/terraform-mcp-server.git`</sub>
- **[dulltz/mcp-server-hcp-terraform](https://github.com/dulltz/mcp-server-hcp-terraform)** — MCP server for working with HashiCorp Cloud Platform (HCP) Terraform, enabling AI assistants to interact with Terraform Cloud resources
  <sub>★ 1 · Python · MIT · source · pushed 2025-04-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dulltz/mcp-server-hcp-terraform.git`</sub>
- **[guilhermeyoshida/mcp-terraform-assistant](https://github.com/guilhermeyoshida/mcp-terraform-assistant)** — An MCP server for managing infrastructure as code using Terraform
  <sub>★ 1 · Python · MIT · source · pushed 2025-04-08 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/guilhermeyoshida/mcp-terraform-assistant.git`</sub>
- **[westonplatter/mcp-terraform-python](https://github.com/westonplatter/mcp-terraform-python)** — MCP server to run terraform operations locally
  <sub>★ 1 · Python · BSD-3-Clause · source · pushed 2025-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/westonplatter/mcp-terraform-python.git`</sub>
- **[pulumi/mcp-server](https://github.com/pulumi/mcp-server)** — MCP server for interacting with Pulumi using the Pulumi Automation API and Pulumi Cloud API. Enables MCP clients to perform Pulumi operations like retrieving package information, previewing changes, deploying updates, and retrieving stack outputs programmatically
  <sub>unavailable</sub>
- **[thrash888/terraform-mcp-server](https://github.com/thrash888/terraform-mcp-server)** — Terraform Registry MCP Server for interacting with Terraform registries
  <sub>unavailable</sub>

## Database Management

- **[haymon-ai/database](https://github.com/haymon-ai/dbmcp)** — Single-binary MCP server for MySQL, MariaDB, PostgreSQL &amp; SQLite with zero runtime dependencies
  <sub>★ 32 · Rust · MIT · psh · pushed 2026-09-18 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://dbmcp.haymon.ai/install.ps1 | iex`</sub>

## Version Control

- **[github/github-mcp-server](https://github.com/github/github-mcp-server)** — Official GitHub server for integration with repository management, PRs, issues, and more
  <sub>★ 33.1k · Go · MIT · source · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/github/github-mcp-server.git`</sub>
- **[adhikasp/mcp-git-ingest](https://github.com/adhikasp/mcp-git-ingest)** — Read and analyze GitHub repositories with your LLM
  <sub>★ 314 · Python · MIT · source · pushed 2025-01-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/adhikasp/mcp-git-ingest.git`</sub>
- **[kopfrechner/gitlab-mr-mcp](https://github.com/kopfrechner/gitlab-mr-mcp)** — Interact seamlessly with issues and merge requests of your GitLab projects
  <sub>★ 94 · JavaScript · MIT · source · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kopfrechner/gitlab-mr-mcp.git`</sub>
- **[ddukbg/github-enterprise-mcp](https://github.com/ddukbg/github-enterprise-mcp)** — MCP server for GitHub Enterprise API integration
  <sub>★ 29 · TypeScript · npx · pushed 2025-09-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @ddukbg/github-enterprise-mcp --token=your_github_token --github-enterprise-url=https://github.your-company.com/api/v3`</sub>
- **[zach-snell/bbkt](https://github.com/zach-snell/bbkt)** — Bitbucket Cloud CLI and MCP server. Manages workspaces, repos, PRs, pipelines, issues, and source code. Token introspection hides tools the API key can't use
  <sub>★ 4 · Go · Apache-2.0 · script · pushed 2026-07-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/zach-snell/bbkt/main/install.sh | bash`</sub>
- **[gitea/gitea-mcp](https://gitea.com/gitea/gitea-mcp)** — Interactive with Gitea instances with MCP
  <sub>website</sub>
  <sub>`https://gitea.com/gitea/gitea-mcp`</sub>
- **[modelcontextprotocol/server-git](https://github.com/modelcontextprotocol/servers/tree/main/server-git)** — Direct Git repository operations including reading, searching, and analyzing local repositories
  <sub>TypeScript · in-repo · pushed 2026-09-03</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/server-git`</sub>
- **[modelcontextprotocol/server-gitlab](https://github.com/modelcontextprotocol/servers/tree/main/server-gitlab)** — GitLab platform integration for project management and CI/CD operations
  <sub>TypeScript · in-repo · pushed 2026-09-03</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/server-gitlab`</sub>
- **[oschina/mcp-gitee](https://github.com/oschina/gitee)** — Gitee API integration, repository, issue, and pull request management, and more
  <sub>unavailable</sub>
- **[rog0x/mcp-git-tools](https://github.com/rog0x/mcp-git-tools)** — Git log analysis, blame, diff viewer, branch management, and repository statistics
  <sub>TypeScript · MIT · source · pushed 2026-03-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rog0x/mcp-git-tools.git`</sub>

## Command Line

- **[wonderwhy-er/DesktopCommanderMCP](https://github.com/wonderwhy-er/DesktopCommanderMCP)** — A swiss-army-knife that can manage/execute programs and read/write/search/edit code and text files
  <sub>★ 9.7k · TypeScript · MIT · npx · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @wonderwhy-er/desktop-commander@latest setup`</sub>
- **[ferrislucas/iterm-mcp](https://github.com/ferrislucas/iterm-mcp)** — A Model Context Protocol server that provides access to iTerm. You can run commands and ask questions about what you see in the iTerm terminal
  <sub>★ 568 · TypeScript · MIT · npx · pushed 2025-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install iterm-mcp --client claude`</sub>
- **[g0t4/mcp-server-commands](https://github.com/g0t4/mcp-server-commands)** — Run any command with run_command and run_script tools
  <sub>★ 233 · TypeScript · MIT · uv · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcpo --port 3010 --api-key "supersecret" -- npx mcp-server-commands`</sub>
- **[tumf/mcp-shell-server](https://github.com/tumf/mcp-shell-server)** — A secure shell command execution server implementing the Model Context Protocol (MCP)
  <sub>★ 195 · Python · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-shell-server --client claude`</sub>
- **[MladenSU/cli-mcp-server](https://github.com/MladenSU/cli-mcp-server)** — Command line interface with secure execution and customizable security policies
  <sub>★ 178 · Python · MIT · npx · pushed 2025-07-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @smithery/cli install cli-mcp-server --client claude`</sub>
- **[automateyournetwork/pyATS_MCP](https://github.com/automateyournetwork/pyATS_MCP)** — Cisco pyATS server enabling structured, model-driven interaction with network devices
  <sub>★ 86 · Python · MIT · clone · pushed 2026-09-16 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/automateyournetwork/pyATS_MCP`</sub>
- **[nylas/cli](https://github.com/nylas/cli)** — Email, calendar, contacts, webhook, timezone, and OTP command-line tool with built-in MCP server support
  <sub>★ 71 · Go · MIT · go · pushed 2026-08-18 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/nylas/cli/cmd/nylas@latest`</sub>
- **[maxim-saplin/mcp_safe_local_python_executor](https://github.com/maxim-saplin/mcp_safe_local_python_executor)** — Safe Python interpreter based on HF Smolagents LocalPythonExecutor
  <sub>★ 48 · Python · MIT · npx · pushed 2025-07-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @maxim-saplin/mcp_safe_local_python_executor --client claude`</sub>
- **[YawLabs/tailscale-mcp](https://github.com/YawLabs/tailscale-mcp)** — Manage Tailscale tailnets with 52 tools for devices, ACL policies, DNS, auth keys, users, webhooks, and audit logs
  <sub>★ 29 · TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx -y @yawlabs/tailscale-mcp@latest validate-acl tailscale/acl.json`</sub>
- **[OthmaneBlial/term_mcp_deepseek](https://github.com/OthmaneBlial/term_mcp_deepseek)** — A DeepSeek MCP-like Server for Terminal
  <sub>★ 18 · Python · MIT · pipx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pipx install "git+https://github.com/OthmaneBlial/term_mcp_deepseek.git@v1.0.0"`</sub>
- **[muchiny/mcp-ssh-bridge](https://github.com/muchiny/bridge-mcp)** — Secure SSH bridge for AI-powered remote server management. 338 tools across 74 groups for Linux, Windows, Docker, Kubernetes, and more. 13 protocol adapters (SSH, WinRM, Telnet, K8s Exec, AWS SSM, Azure, GCP), server-side output filtering, and 6,300+ tests
  <sub>★ 8 · Rust · MIT · clone · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/muchiny/bridge-mcp`</sub>
- **[claw-army/claude-node](https://github.com/claw-army/claude-node)** — Python subprocess bridge for Claude Code CLI, giving Python code direct access to Claude Code native capabilities via stream-json
  <sub>★ 6 · Python · pip · pushed 2026-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install claude-node`</sub>

## Security

- **[LaurieWired/GhidraMCP](https://github.com/LaurieWired/GhidraMCP)** — A Model Context Protocol server for Ghidra that enables LLMs to autonomously reverse engineer applications. Provides tools for decompiling binaries, renaming methods and data, and listing methods, classes, imports, and exports
  <sub>★ 10.1k · Java · Apache-2.0 · source · pushed 2025-06-23</sub>
  <sub>`git clone https://github.com/LaurieWired/GhidraMCP.git`</sub>
- **[microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit)** — Kernel-level governance MCP server for AI agents. Provides deterministic policy enforcement, compliance checking (SOC2, GDPR, HIPAA), audit logging (SQLite-based), and human-in-the-loop approvals. Install via pip install agent-os-kernel
  <sub>★ 6.3k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @microsoft/agent-governance-copilot-cli install`</sub>
- **[prompt-security/clawsec](https://github.com/prompt-security/clawsec)** — Security audit platform for AI agent skills and MCP servers. Five-tier detection pipeline (core rules, dynamic rules, LLM analysis, Firecracker sandbox, LLM review), continuous rule evolution, and automated vulnerability reports
  <sub>★ 1.1k · JavaScript · AGPL-3.0 · npx · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx skills add prompt-security/clawsec --skill clawsec-suite -a openclaw --global -y`</sub>
- **[luckyPipewrench/pipelock](https://github.com/luckyPipewrench/pipelock)** — Firewall for AI agents that wraps MCP servers with bidirectional scanning for credential leaks, prompt injection, and tool poisoning detection. Also provides an HTTP fetch proxy with a 9-layer scanner pipeline
  <sub>★ 894 · Go · Apache-2.0 · brew · pushed 2026-09-21 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`brew install luckyPipewrench/tap/pipelock`</sub>
- **[semgrep/mcp](https://github.com/semgrep/mcp)** — Allow AI agents to scan code for security vulnerabilites using Semgrep
  <sub>★ 688 · Python · MIT · uv · pushed 2025-10-28 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx semgrep-mcp # see --help for more options`</sub>
- **[cordum-io/cordum](https://github.com/cordum-io/cordum)** — Safety-first agent control plane with pre-dispatch policy evaluation (deny/escalate/allow), output scanning (PII, secrets, injection), job scheduling, and full audit trail. Native MCP server with stdio and HTTP/SSE transport
  <sub>★ 508 · Go · helm · pushed 2026-09-17 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`helm install cordum oci://ghcr.io/cordum-io/cordum/charts/cordum \`</sub>
- **[securityfortech/secops-mcp](https://github.com/securityfortech/secops-mcp)** — All-in-one security testing toolbox that brings together popular open source tools through a single MCP interface. Connected to an AI agent, it enables tasks like pentesting, bug bounty hunting, threat hunting, and more
  <sub>★ 213 · Python · MIT · docker · pushed 2025-09-17 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`docker run -it --rm secops-mcp`</sub>
- **[BurtTheCoder/mcp-shodan](https://github.com/w0h1v/mcp-shodan)** — MCP server for querying the Shodan API and Shodan CVEDB. This server provides tools for IP lookups, device searches, DNS lookups, vulnerability queries, CPE lookups, and more
  <sub>★ 172 · TypeScript · MIT · npm · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @burtthecoder/mcp-shodan`</sub>
- **[BurtTheCoder/mcp-virustotal](https://github.com/w0h1v/mcp-virustotal)** — MCP server for querying the VirusTotal API. This server provides tools for scanning URLs, analyzing file hashes, and retrieving IP address reports
  <sub>★ 149 · TypeScript · MIT · npm · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @burtthecoder/mcp-virustotal`</sub>
- **[13bm/GhidraMCP](https://github.com/13bm/GhidraMCP)** — MCP server for integrating Ghidra with AI assistants. This plugin enables binary analysis, providing tools for function inspection, decompilation, memory exploration, and import/export analysis via the Model Context Protocol
  <sub>★ 140 · Java · Apache-2.0 · clone · pushed 2026-09-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/13bm/GhidraMCP.git`</sub>
- **[roadwy/cve-search_mcp](https://github.com/roadwy/cve-search_mcp)** — A Model Context Protocol (MCP) server for querying the CVE-Search API. This server provides comprehensive access to CVE-Search, browse vendor and product、get CVE per CVE-ID、get the last updated CVEs
  <sub>★ 107 · Python · MIT · clone · pushed 2025-07-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/roadwy/cve-search_mcp.git`</sub>
- **[qianniuspace/mcp-security-audit](https://github.com/qianniuspace/mcp-security-audit)** — A powerful MCP (Model Context Protocol) Server that audits npm package dependencies for security vulnerabilities. Built with remote npm registry integration for real-time security checks
  <sub>★ 57 · TypeScript · MIT · npx · pushed 2025-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @qianniuspace/mcp-security-audit --client claude`</sub>
- **[girste/mcp-cybersec-watchdog](https://github.com/girste/CHIHUAUDIT)** — Comprehensive security audit tool for Linux servers. Analyzes firewall, SSH hardening, threats, fail2ban, Docker, kernel hardening. Returns actionable recommendations with zero configuration
  <sub>★ 53 · Go · MIT · source · pushed 2026-02-07 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/girste/mcp-cybersec-watchdog.git`</sub>
- **[fr0gger/MCP_Security](https://github.com/fr0gger/MCP_Security)** — MCP server for querying the ORKL API. This server provides tools for fetching threat reports, analyzing threat actors, and retrieving intelligence sources
  <sub>★ 51 · Python · source · pushed 2025-01-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fr0gger/MCP_Security.git`</sub>
- **[slouchd/cyberchef-api-mcp-server](https://github.com/slouchd/cyberchef-api-mcp-server)** — MCP server for interacting with the CyberChef server API which will allow an MCP client to utilise the CyberChef operations
  <sub>★ 44 · Python · MIT · source · pushed 2026-04-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/slouchd/cyberchef-api-mcp-server.git`</sub>
- **[nickpending/mcp-recon](https://github.com/nickpending/mcp-recon)** — Conversational recon interface and MCP server powered by httpx and asnmap. Supports various reconnaissance levels for domain analysis, security header inspection, certificate analysis, and ASN lookup
  <sub>★ 30 · Go · clone · pushed 2025-04-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/nickpending/mcp-recon.git`</sub>
- **[IgorGanapolsky/ThumbGate](https://github.com/IgorGanapolsky/ThumbGate)** — Pre-action gates for AI coding agents, blocking risky or repeated mistakes before they affect code or systems
  <sub>★ 26 · JavaScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx thumbgate init # Phase 1: hooks only`</sub>
- **[operantlabs/operant-mcp](https://github.com/operantlabs/operant-mcp)** — Security testing MCP server with 51 tools for penetration testing, network forensics, memory analysis, and vulnerability assessment. Install via npx operant-mcp
  <sub>★ 23 · TypeScript · MIT · npm · pushed 2026-04-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g operant-mcp`</sub>
- **[aak204/MCP-Trust-Kit](https://github.com/aak204/MCP-Scorecard)** — Deterministic CI scanner and surface-risk scoring for MCP servers
  <sub>★ 21 · Python · Apache-2.0 · gh-action · pushed 2026-04-09</sub>
  <sub>`uses: aak204/MCP-Trust-Kit@main # in .github/workflows/*.yml`</sub>
- **[icoretech/warden-mcp](https://github.com/icoretech/warden-mcp)** — MCP server for Bitwarden and Vaultwarden vault management. Search, create, edit, and organize logins, notes, cards, identities, SSH keys, folders, collections, attachments, and Sends via the official bw CLI
  <sub>★ 16 · TypeScript · MIT · npm · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @bitwarden/cli@2026.8.0`</sub>
- **[elliotllliu/agent-shield](https://github.com/elliotllliu/agent-shield)** — Pre-deployment security scanner for AI agent skills, MCP servers, and plugins. 30 detection rules with AST taint tracking, cross-file data flow analysis, and multi-language prompt injection detection (8 languages). CI/CD integration via GitHub Action. Zero install via npx, 100% offline
  <sub>★ 15 · TypeScript · MIT · npm · pushed 2026-03-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @elliotllliu/agent-shield`</sub>
- **[sidclawhq/platform](https://github.com/sidclawhq/platform)** — Governance proxy for MCP servers with identity, policy evaluation, human approval, and traceability for agent actions
  <sub>★ 14 · TypeScript · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx sidclaw-demo`</sub>
- **[takleb3rry/zitadel-mcp](https://github.com/takleb3rry/zitadel-mcp)** — /🏠 - MCP server for Zitadel identity management — manage users, projects, OIDC apps, roles, and service accounts through natural language. Supports user lifecycle, RBAC, and OIDC configuration
  <sub>★ 10 · TypeScript · MIT · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/takleb3rry/zitadel-mcp.git`</sub>
- **[artvepa80/Agents-Hefesto](https://github.com/artvepa80/Agents-Hefesto)** — Code quality and security review MCP server for AI-generated code, including semantic drift, complexity, and vulnerability analysis
  <sub>★ 7 · Python · npx · pushed 2026-05-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @smithery/cli@latest mcp add artvepa80/hefestoai`</sub>
- **[rad-security/mcp-server](https://github.com/rad-security/mcp-server)** — MCP server for RAD Security, providing AI-powered security insights for Kubernetes and cloud environments. This server provides tools for querying the Rad Security API and retrieving security findings, reports, runtime data and many more
  <sub>★ 6 · TypeScript · MIT · source · pushed 2026-09-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/rad-security/mcp-server.git`</sub>
- **[ExposureGuard/haldir](https://github.com/ExposureGuard/haldir)** — Agent security layer for scoped sessions, secrets, audit trails, and proxy-based tool-call review
  <sub>★ 4 · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install haldir`</sub>
- **[JoeyBrar/agentseal-mcp](https://github.com/JoeyBrar/agentseal-mcp)** — Action logs for AI agents. Records every action in a SHA-256 hash chain, for verifiable audit trails. Install via npx agentseal-mcp
  <sub>★ 1 · JavaScript · MIT · pip · pushed 2026-04-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentseal-sdk`</sub>
- **[bottobot/defense-mcp-server](https://github.com/bottobot/defense-mcp-server)** — 31 defensive security tools with 250+ actions for Linux system hardening, compliance auditing, firewall management, vulnerability scanning, and incident response. Dry-run by default
  <sub>unavailable</sub>
- **[wd041216-bit/ironclaw-agent-guard](https://github.com/wd041216-bit/ironclaw-agent-guard)** — Agent-runtime security guard with stdio and Streamable HTTP MCP servers. Exposes security_scan and redact_text for risky tool payload review, prompt-injection checks, secret redaction, and JSONL audit logging
  <sub>unavailable</sub>
- **[PolicyLayer/Intercept](https://github.com/PolicyLayer/Intercept)** — Open-source MCP proxy that enforces YAML policies on every tool call. Rate limiting, spending caps, argument validation, and full audit logging at the transport layer. Works with any MCP server
  <sub>unavailable</sub>
- **[Sentinel-Gate/Sentinelgate](https://github.com/Sentinel-Gate/Sentinelgate)** — Open-source MCP proxy for AI agent access control. Intercepts every tool call with CEL policies, RBAC, full audit trail, content scanning, and Admin UI. Single binary, zero dependencies
  <sub>unavailable</sub>
- **[brainAI-bot/agentfolio-mcp-server](https://github.com/brainAI-bot/agentfolio-mcp-server)** — Agent identity and trust-verification MCP server for AI-agent discovery and DevOps workflow governance
  <sub>JavaScript · MIT · npm · pushed 2026-03-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g github:brainAI-bot/agentfolio-mcp-server`</sub>
- **[shadoprizm/cyberlens-mcp-server](https://github.com/shadoprizm/cyberlens-mcp-server)** — Security scanning MCP server for websites, GitHub repositories, and MCP/OpenClaw skills from AI assistants
  <sub>TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @shadoprizm/cyberlens-mcp-server`</sub>
- **[arcjet/mcp](https://docs.arcjet.com/mcp-server)** — Runtime security platform for AI applications, including budget enforcement, prompt-injection protection, bot detection, and PII controls
  <sub>website</sub>
  <sub>`https://docs.arcjet.com/mcp-server`</sub>
- **[Scottpedia0/access](https://github.com/Scottpedia0/access)** — Self-hosted credential store, API proxy, and MCP server that lets agents access services through one controlled bearer token
  <sub>TypeScript · MIT · clone · pushed 2026-04-06 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Scottpedia0/access.git`</sub>
- **[ExposureGuard/exposureguard-mcp](https://github.com/ExposureGuard/exposureguard-mcp)** — Domain security scanning MCP server for SPF, DMARC, SSL, headers, DNSSEC, and open-port checks with remediation guidance
  <sub>Python · npx · pushed 2026-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx exposureguard-mcp`</sub>
- **[matthiastjong/shellgate](https://github.com/matthiastjong/shellgate)** — /🏠 - Self-hosted secure gateway for AI agents with scoped tokens, credential injection, human review, SSH execution, and audit trails
  <sub>unavailable</sub>

## Testing &amp; Chaos Engineering

- **[ai-dashboad/flutter-skill](https://github.com/ai-dashboad/flutter-skill)** — AI-powered E2E testing bridge for any app. Supports Flutter, iOS, Android, Web, Electron, Tauri, KMP, React Native, .NET MAUI
  <sub>★ 375 · Dart · MIT · scoop · pushed 2026-09-01 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`scoop install flutter-skill`</sub>
- **[Typewise/mcp-chaos-rig](https://github.com/Typewise/mcp-chaos-rig)** — A local MCP server that breaks on demand. Test your client against auth failures, disappearing tools, flaky responses, and token expiry, all from a web UI
  <sub>★ 10 · TypeScript · MIT · npm · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-chaos-rig`</sub>
- **[rog0x/mcp-log-tools](https://github.com/rog0x/mcp-log-tools)** — Log parsing, pattern detection, error extraction, log statistics, and anomaly detection
  <sub>★ 1 · TypeScript · source · pushed 2026-03-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rog0x/mcp-log-tools.git`</sub>
- **[autonomous-testing/wopee-mcp](https://www.npmjs.com/package/wopee-mcp)** — AI testing agents for web apps — dispatch test runs, analysis crawls, and AI agent tests, fetch artifacts and project status
  <sub>website</sub>
  <sub>`https://www.npmjs.com/package/wopee-mcp`</sub>
- **[rog0x/mcp-testing-tools](https://github.com/rog0x/mcp-testing-tools)** — Unit test generation, coverage analysis, test planning, fixture generation, and mutation testing suggestions
  <sub>TypeScript · MIT · source · pushed 2026-03-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rog0x/mcp-testing-tools.git`</sub>
- **[rog0x/mcp-perf-tools](https://github.com/rog0x/mcp-perf-tools)** — Benchmarking, profiling, memory analysis, CPU analysis, and load testing
  <sub>TypeScript · source · pushed 2026-03-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rog0x/mcp-perf-tools.git`</sub>

## Code Execution

- **[ckanthony/openapi-mcp](https://github.com/ckanthony/openapi-mcp)** — OpenAPI-MCP: Dockerized MCP Server to allow your AI agent to access any API with existing api docs
  <sub>★ 196 · Go · docker · pushed 2026-03-21 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm openapi-mcp:latest --help`</sub>
- **[alfonsograziano/node-code-sandbox-mcp](https://github.com/alfonsograziano/node-code-sandbox-mcp)** — A Node.js MCP server that spins up isolated Docker-based sandboxes for executing JavaScript snippets with on-the-fly npm dependency installation and clean teardown
  <sub>★ 157 · TypeScript · source · pushed 2025-11-24 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/alfonsograziano/node-code-sandbox-mcp.git`</sub>
- **[yepcode/mcp-server-js](https://github.com/yepcode/mcp-server-js)** — Execute any LLM-generated code in a secure and scalable sandbox environment and create your own MCP tools using JavaScript or Python, with full support for NPM and PyPI packages
  <sub>★ 46 · TypeScript · MIT · source · pushed 2026-03-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/yepcode/mcp-server-js.git`</sub>
- **[pydantic/pydantic-ai/mcp-run-python](https://github.com/pydantic/pydantic-ai/tree/main/packages/mcp-run-python)** — Run Python code in a secure sandbox via MCP tool calls
  <sub>Python · MIT · in-repo · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/pydantic/pydantic-ai.git && cd pydantic-ai/packages/mcp-run-python`</sub>

## Dependency Analysis

- **[arvindand/maven-tools-mcp](https://github.com/arvindand/maven-tools-mcp)** — Universal Maven Central dependency intelligence for JVM build tools (Maven, Gradle, SBT, Mill). Provides version lookups, dependency health checks, age analysis, release patterns, and upgrade guidance with Context7 integration
  <sub>★ 33 · Java · MIT · source · pushed 2026-09-06 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/arvindand/maven-tools-mcp.git`</sub>
- **[tersePrompts/jarp-mcp](https://github.com/tersePrompts/jarp-mcp)** — Java Archive Reader Protocol - MCP server that gives AI agents X-ray vision into compiled Java code. Enables decompiling and analyzing Java classes directly from Maven/Gradle dependencies using bundled CFR decompiler with zero-setup installation
  <sub>★ 7 · TypeScript · Apache-2.0 · npm · pushed 2026-09-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g jarp-mcp`</sub>
- **[lunacompsia-oss/mcp-server-changelog](https://github.com/lunacompsia-oss/mcp-server-changelog)** — Fetch and parse changelogs, release notes, and breaking changes from npm, PyPI, crates.io, and GitHub repositories
  <sub>unavailable</sub>
- **[lunacompsia-oss/mcp-server-deps](https://github.com/lunacompsia-oss/mcp-server-deps)** — Analyze dependency trees, check for vulnerabilities via OSV.dev, and audit outdated packages across npm, PyPI, and crates.io
  <sub>unavailable</sub>
- **[lunacompsia-oss/mcp-server-license](https://github.com/lunacompsia-oss/mcp-server-license)** — Check license types, SPDX compliance, compatibility matrices, and risk classification for open-source dependencies
  <sub>unavailable</sub>

## Continuous Integration

- **[lobehub/mcp-hello-world](https://github.com/lobehub/mcp-hello-world)** — A simple Hello World MCP server for CI/CD test
  <sub>★ 22 · JavaScript · MIT · npx · pushed 2025-06-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-hello-world`</sub>
- **[ratamaha-git/n8n-mcp](https://github.com/AutomateLab-tech/n8n-mcp)** — MCP server for authoring n8n workflows: scaffolds custom node TypeScript skeletons, generates valid workflow JSON from natural-language descriptions, and lints workflows for deprecated node types, missing typeVersion, and broken connections. Ships with a Claude Code skill
  <sub>★ 12 · TypeScript · MIT · npm · pushed 2026-06-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @automatelab/n8n-mcp`</sub>
- **[GeiserX/spinnaker-mcp](https://github.com/GeiserX/spinnaker-mcp)** — A Go-based MCP server that bridges any Spinnaker continuous delivery instance via the Gate API, exposing 37 tools for application management, pipeline operations, execution control, and infrastructure queries
  <sub>★ 5 · Go · GPL-3.0 · npm · pushed 2026-08-24 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g spinnaker-mcp`</sub>
- **[Tiberriver256/mcp-server-github-actions](https://github.com/Tiberriver256/mcp-server-github-actions)** — MCP server for interacting with GitHub Actions workflows, enabling AI assistants to manage CI/CD pipelines
  <sub>unavailable</sub>

## DevOps Visibility

- **[gofireflyio/firefly-mcp](https://github.com/gofireflyio/firefly-mcp)** — Integrates, discovers, manages, and codifies cloud resources with Firefly
  <sub>★ 16 · TypeScript · MIT · npx · pushed 2026-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @fireflyai/firefly-mcp`</sub>
- **[SBDI/mcp-devps-hub](https://github.com/SBDI/mcp-devps-hub)** — MCP server for end-to-end development visibility (Jira, GitHub, CI/CD, etc.)
  <sub>★ 1 · Python · source · pushed 2025-04-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SBDI/mcp-devps-hub.git`</sub>
- **[Acid-base/FastMCP-Proper](https://github.com/Acid-base/FastMCP-Proper)** — Python MCP server with CI/CD tooling and testability built-in
  <sub>★ 1 · Python · MIT · source · pushed 2025-04-25 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/Acid-base/FastMCP-Proper.git`</sub>

## Mobile CI/CD

- **[stefanoamorelli/codemagic-mcp](https://github.com/stefanoamorelli/codemagic-mcp)** — Codemagic CI/CD MCP Server for mobile app CI/CD pipeline management
  <sub>★ 13 · Python · MIT · clone · pushed 2026-05-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stefanoamorelli/codemagic-mcp.git`</sub>

## Browser Automation

- **[microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)** — Official Microsoft Playwright MCP server, enabling LLMs to interact with web pages through structured accessibility snapshots
  <sub>★ 37.4k · TypeScript · Apache-2.0 · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @playwright/mcp@latest --config path/to/config.json`</sub>
- **[browsermcp/mcp](https://github.com/BrowserMCP/mcp)** — Automate your local Chrome browser
  <sub>★ 7.1k · TypeScript · Apache-2.0 · source · pushed 2025-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/browsermcp/mcp.git`</sub>
- **[browserbase/mcp-server-browserbase](https://github.com/browserbase/mcp-server-browserbase)** — Automate browser interactions in the cloud (e.g. web navigation, data extraction, form filling, and more)
  <sub>★ 3.4k · TypeScript · Apache-2.0 · clone · pushed 2026-07-20 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/browserbase/mcp-server-browserbase.git`</sub>
- **[opentabs-dev/opentabs](https://github.com/opentabs-dev/opentabs)** — Plugin-based MCP server for giving AI agents structured access to web applications through the user's browser session
  <sub>★ 955 · TypeScript · MIT · npm · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @opentabs-dev/cli`</sub>
- **[co-browser/browser-use-mcp-server](https://github.com/kontext-security/browser-use-mcp-server)** — browser-use packaged as an MCP server with SSE transport. includes a dockerfile to run chromium in docker + a vnc server
  <sub>★ 843 · Python · MIT · uv · pushed 2026-05-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install dist/browser_use_mcp_server-*.whl`</sub>
- **[eyalzh/browser-control-mcp](https://github.com/eyalzh/browser-control-mcp)** — An MCP server paired with a browser extension that enables LLM clients to control the user's browser (Firefox)
  <sub>★ 323 · TypeScript · MIT · source · pushed 2026-08-23 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/eyalzh/browser-control-mcp.git`</sub>
- **[Automata-Labs-team/MCP-Server-Playwright](https://github.com/VikashLoomba/MCP-Server-Playwright)** — An MCP server for browser automation using Playwright
  <sub>★ 299 · JavaScript · MIT · npx · pushed 2025-06-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @automatalabs/mcp-server-playwright --client claude`</sub>
- **[achiya-automation/safari-mcp](https://github.com/achiya-automation/safari-mcp)** — Native Safari browser automation for AI agents on macOS, including navigation, interaction, screenshots, network inspection, and accessibility snapshots
  <sub>★ 204 · JavaScript · MIT · npm · pushed 2026-09-21 · macOS</sub>
  <sub>`npm install -g safari-mcp`</sub>
- **[blackwhite084/playwright-plus-python-mcp](https://github.com/blackwhite084/playwright-plus-python-mcp)** — An MCP python server using Playwright for browser automation, more suitable for llm
  <sub>★ 189 · Python · Apache-2.0 · npx · pushed 2025-01-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv --directory C:\Users\YUNYING\Documents\project\python\mcp\playwright-server run playwright-server`</sub>
- **[ndthanhdev/mcp-browser-kit](https://github.com/ndthanhdev/mcp-browser-kit)** — An MCP Server for interacting with manifest v2 compatible browsers
  <sub>★ 54 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @mcp-browser-kit/server@latest --transport http`</sub>
- **[mcpware/pagecast](https://github.com/mcpware/pagecast)** — MCP server that records browser sessions as GIF/video using Playwright and ffmpeg — AI-driven QA evidence and demo recording
  <sub>★ 48 · JavaScript · MIT · npx · pushed 2026-03-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @mcpware/pagecast`</sub>
- **[kimtth/mcp-aoai-web-browsing](https://github.com/kimtth/mcp-aoai-web-browsing)** — A minimal server/client MCP implementation using Azure OpenAI and Playwright
  <sub>★ 35 · Python · MIT · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kimtth/mcp-aoai-web-browsing.git`</sub>
- **[mcpware/ui-annotator-mcp](https://github.com/mcpware/ui-annotator-mcp)** — MCP server that annotates web pages with hover labels for AI assistants — reverse proxy injects annotations, zero browser extensions needed
  <sub>★ 17 · JavaScript · MIT · npx · pushed 2026-03-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @mcpware/ui-annotator`</sub>
- **[aircodelabs/grasp](https://github.com/aircodelabs/grasp)** — Self-hosted browser using agent with built-in MCP and A2A support
  <sub>★ 5 · TypeScript · Apache-2.0 · source · pushed 2025-06-20 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/aircodelabs/grasp.git`</sub>
- **[kc23go/anybrowse](https://github.com/kc23go/anybrowse)** — Web scraping MCP server for AI agents using managed Chrome, with npm package and hosted service options
  <sub>★ 5 · TypeScript · MIT · source · pushed 2026-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kc23go/anybrowse.git`</sub>
- **[Custodia-Admin/pagebolt-mcp](https://github.com/Custodia-Admin/pagebolt-mcp)** — Hosted web capture MCP server: screenshots, PDFs, narrated video recording, and page inspection for DevOps pipelines. No infrastructure required
  <sub>★ 4 · JavaScript · MIT · source · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Custodia-Admin/pagebolt-mcp.git`</sub>
- **[executeautomation/mcp-playwright-server](https://github.com/executeautomation/playwright-mcp-server)** — An MCP server using Playwright for browser automation and webscrapping
  <sub>unavailable</sub>
- **[getrupt/ashra-mcp](https://github.com/getrupt/ashra-mcp)** — Extract structured data from any website. Just prompt and get JSON
  <sub>unavailable</sub>
- **[modelcontextprotocol/server-puppeteer](https://github.com/modelcontextprotocol/servers/tree/main/server-puppeteer)** — Browser automation for web scraping and interaction
  <sub>TypeScript · in-repo · pushed 2026-09-03</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/server-puppeteer`</sub>
- **[plasmate-labs/plasmate-mcp](https://github.com/plasmate-labs/plasmate-mcp)** — MCP server for Plasmate web-content capture and processing workflows in AI coding assistants
  <sub>JavaScript · Apache-2.0 · npm · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g plasmate-mcp`</sub>

## Coding Agents

- **[oraios/serena](https://github.com/oraios/serena)** — A fully-featured coding agent that relies on symbolic code operations by using language servers
  <sub>★ 29.7k · Python · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install -p 3.13 serena-agent`</sub>
- **[ezyang/codemcp](https://github.com/ezyang/codemcp)** — Coding agent with basic read, write and command line tools
  <sub>★ 1.6k · Python · Apache-2.0 · uv · pushed 2025-12-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from git+https://github.com/ezyang/codemcp@prod codemcp serve`</sub>
- **[sipyourdrink-ltd/bernstein](https://github.com/sipyourdrink-ltd/bernstein)** — Multi-agent CLI coding orchestrator with worktree isolation, model routing, quality gates, and audit logging
  <sub>★ 1.2k · Python · Apache-2.0 · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install bernstein # or: pipx install bernstein`</sub>
- **[bgauryy/octocode-mcp](https://github.com/bgauryy/octocode)** — AI-powered developer assistant that enables advanced research, analysis and discovery across GitHub ecosystem
  <sub>★ 942 · TypeScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx octocode --help`</sub>
- **[juehang/vscode-mcp-server](https://github.com/juehang/vscode-mcp-server)** — A MCP Server that allows AI such as Claude to read from the directory structure in a VS Code workspace, see problems picked up by linter(s) and the language server, read code files, and make edits
  <sub>★ 394 · TypeScript · MIT · source · pushed 2026-01-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/juehang/vscode-mcp-server.git`</sub>
- **[cafeTechne/antigravity-link-extension](https://github.com/cafeTechne/antigravity-link-extension)** — Mobile companion and MCP/OpenAPI bridge for Google's Antigravity IDE, enabling remote session viewing and control
  <sub>★ 212 · HTML · MIT · source · pushed 2026-06-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cafeTechne/antigravity-link-extension.git`</sub>
- **[scrapeless/mcp-server-scrapeless](https://github.com/scrapeless-ai/scrapeless-mcp-server)** — Seamlessly integrate real-time Google SERP(Google Search, Google Flight, Google Map, Google Jobs....) results into your LLM applications using the Scrapeless MCP server
  <sub>★ 169 · TypeScript · MIT · source · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/scrapeless-ai/scrapeless-mcp-server.git`</sub>
- **[jinzcdev/leetcode-mcp-server](https://github.com/jinzcdev/leetcode-mcp-server)** — MCP server enabling automated access to LeetCode's programming problems, solutions, submissions and public data with optional authentication for user-specific features (e.g., notes), supporting both leetcode.com (global) and leetcode.cn (China) sites
  <sub>★ 149 · TypeScript · MIT · npx · pushed 2026-07-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @jinzcdev/leetcode-mcp-server --site global`</sub>
- **[blackwell-systems/agent-lsp](https://github.com/blackwell-systems/agent-lsp)** — MCP server providing language server intelligence for code analysis, navigation, and refactoring across 30 languages. Includes speculative execution (simulate edits before applying), blast-radius analysis, and three-layer verification. 56 tools, single Go binary
  <sub>★ 133 · Go · MIT · winget · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`winget install BlackwellSystems.agent-lsp`</sub>
- **[doggybee/mcp-server-leetcode](https://github.com/doggybee/mcp-server-leetcode)** — An MCP server that enables AI models to search, retrieve, and solve LeetCode problems. Supports metadata filtering, user profiles, submissions, and contest data access
  <sub>★ 43 · TypeScript · MIT · npm · pushed 2025-04-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @mcpfun/mcp-server-leetcode`</sub>
- **[Wolfe-Jam/claude-faf-mcp](https://github.com/Wolfe-Jam/claude-faf-mcp)** — Persistent Project Context for Claude — IANA-registered .faf format · Core 14 MCP tools (30 with FAF_TOOLS=all) + 2 prompts · MCP Registry #2759
  <sub>★ 23 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claude-faf-mcp`</sub>
- **[williamzujkowski/nexus-agents](https://github.com/nexus-substrate/nexus-agents)** — Multi-CLI AI coding-agent orchestration with consensus review, governance rules, telemetry, and development-pipeline workflows
  <sub>★ 18 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g nexus-agents`</sub>
- **[HendryAvila/Hoofy](https://github.com/HendryAvila/Hoofy)** — Spec-driven development companion with persistent memory (SQLite + FTS5 + knowledge graph), adaptive change pipeline (12 flow variants), greenfield project pipeline with Clarity Gate, and business rules extraction. 32 MCP tools. Single Go binary, zero dependencies
  <sub>★ 15 · Go · MIT · psh · pushed 2026-03-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/HendryAvila/Hoofy/main/install.ps1 | iex`</sub>
- **[Wolfe-Jam/faf-mcp](https://github.com/Wolfe-Jam/faf-mcp)** — Universal persistent project context for Cursor, Windsurf, Cline, VS Code, and all MCP-compatible platforms (including Claude Desktop). IANA-registered format (application/vnd.faf+yaml). 17 native tools, AI-readiness scoring
  <sub>★ 7 · TypeScript · MIT · npx · pushed 2026-09-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`bunx faf-mcp`</sub>

## Aggregators

- **[mindsdb/mindsdb](https://github.com/mindsdb/mindshub)** — Connect and unify data across various platforms and databases with MindsDB as a single MCP server
  <sub>★ 39.8k · Makefile · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mindsdb/mindsdb.git`</sub>
- **[metatool-ai/metatool-app](https://github.com/metatool-ai/metamcp)** — MetaMCP is the one unified middleware MCP server that manages your MCP connections with GUI
  <sub>★ 2.7k · TypeScript · MIT · clone · pushed 2026-06-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/metatool-ai/metamcp.git`</sub>
- **[julien040/anyquery](https://github.com/julien040/anyquery)** — Query more than 40 apps with one binary using SQL. It can also connect to your PostgreSQL, MySQL, or SQLite compatible database. Local-first and private by design
  <sub>★ 1.8k · Go · winget · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install JulienCagniart.anyquery`</sub>
- **[smart-mcp-proxy/mcpproxy-go](https://github.com/smart-mcp-proxy/mcpproxy-go)** — Local MCP proxy that aggregates multiple servers behind a single endpoint. Features BM25 tool discovery, quarantine security, activity logging, Docker isolation, and web UI
  <sub>★ 376 · Go · MIT · go · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/smart-mcp-proxy/mcpproxy-go/cmd/mcpproxy@latest`</sub>
- **[wegotdocs/open-mcp](https://github.com/boltmcp/boltmcp)** — Turn a web API into an MCP server in 10 seconds and add it to the open source registry: https://open-mcp.org
  <sub>★ 371 · Shell · source · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/wegotdocs/open-mcp.git`</sub>
- **[sxhxliang/mcp-access-point](https://github.com/sxhxliang/mcp-access-point)** — Turn a web service into an MCP server in one click without making any code changes
  <sub>★ 184 · Rust · MIT · docker · pushed 2026-03-11 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -d --name mcp-access-point --rm \`</sub>
- **[VeriTeknik/pluggedin-mcp-proxy](https://github.com/VeriTeknik/pluggedin-mcp-proxy)** — A comprehensive proxy server that combines multiple MCP servers into a single interface with extensive visibility features. It provides discovery and management of tools, prompts, resources, and templates across servers, plus a playground for debugging when building MCP servers
  <sub>★ 135 · TypeScript · Apache-2.0 · npx · pushed 2026-05-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @pluggedin/pluggedin-mcp-proxy@latest --pluggedin-api-key YOUR_API_KEY`</sub>
- **[juspay/neurolink](https://github.com/juspay/neurolink)** — TypeScript-first AI SDK that unifies 13 major AI providers and 100+ models under a single consistent API. Connects to remote MCP servers via addExternalMCPServer/addMCPServer APIs with built-in HTTP-based MCP connection, auth, retries, and rate limiting
  <sub>★ 135 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @juspay/neurolink --help`</sub>
- **[askbudi/roundtable](https://github.com/yylo-dev/roundtable)** — Zero-configuration MCP server that unifies multiple AI coding assistants (Codex, Claude Code, Cursor, Gemini) through intelligent auto-discovery and standardized interface
  <sub>★ 125 · Python · npx · pushed 2025-10-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @roundtable/mcp-server`</sub>
- **[WayStation-ai/mcp](https://github.com/waystation-ai/mcp)** — Seamlessly and securely connect Claude Desktop and other MCP hosts to your favorite apps (Notion, Slack, Monday, Airtable, etc.). Takes less than 90 secs
  <sub>★ 63 · JavaScript · source · pushed 2025-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/waystation-ai/mcp.git`</sub>
- **[glenngillen/mcpmcp-server](https://github.com/glenngillen/mcpmcp-server)** — A list of MCP servers so you can ask your client which servers you can use to improve your daily workflow
  <sub>★ 38 · Apache-2.0 · source · pushed 2025-04-24 · macOS?</sub>
  <sub>`git clone https://github.com/glenngillen/mcpmcp-server.git`</sub>
- **[BytesAgain](https://github.com/bytesagain/ai-skills)** — Searchable AI-agent skill catalog exposed through MCP SSE and REST APIs
  <sub>★ 14 · Shell · source · pushed 2026-04-26</sub>
  <sub>`git clone https://github.com/bytesagain/ai-skills.git`</sub>
- **[unitedideas/nothumansearch](https://github.com/unitedideas/nothumansearch)** — MCP server for discovering agent-first tools and checking agentic readiness signals across indexed sites
  <sub>★ 8 · Go · MIT · source · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/unitedideas/nothumansearch.git`</sub>
- **[supertrained/rhumb](https://github.com/supertrained/rhumb)** — API discovery and scoring for AI agents, with service scoring and governed capability routing for external APIs
  <sub>★ 4 · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y --package rhumb-mcp@latest rhumb-mcp`</sub>
- **[lazymac/mcp](https://github.com/lazymac2x/lazymac-mcp)** — Unified MCP server exposing developer utilities such as QR generation, IP geolocation, AI cost helpers, LLM routing, and privacy tooling
  <sub>★ 3 · JavaScript · MIT · npx · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @lazymac/mcp --client claude`</sub>
- **[SkillFlow](https://github.com/rafsilva85/skillflow-mcp-server)** — Open marketplace for AI agent skills. Discover 500+ MCP servers and automation tools, compare capabilities, and deploy to your AI stack. Free and open source
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-03-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g skillflow-mcp-server`</sub>
- **[uAI-solana/useful-ai-mcp](https://github.com/uAI-solana/useful-ai-mcp)** — Fully dynamic MCP server exposing 200+ shared utility tools for AI agents. Tool list updates automatically based on real usage data. No auth required
  <sub>★ 1 · source · pushed 2026-03-24</sub>
  <sub>`git clone https://github.com/uAI-solana/useful-ai-mcp.git`</sub>
- **[Composiohq/Rube](https://github.com/composiohq/rube)** — Rube is an MCP server built on the Composio integration platform. It connects your AI tools to 500+ apps
  <sub>unavailable</sub>
- **[PipedreamHQ/pipedream](https://github.com/PipedreamHQ/pipedream/tree/master/packages/mcp-server)** — Connect with 2,500 APIs with 8,000+ prebuilt tools, and manage servers for your users, in your own app
  <sub>JavaScript · in-repo · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/PipedreamHQ/pipedream.git && cd pipedream/packages/mcp-server`</sub>
- **[tigranbs/mcgravity](https://github.com/tigranbs/mcgravity)** — A proxy tool for composing multiple MCP servers into one unified endpoint. Scale your AI tools by load balancing requests across multiple MCP servers, similar to how Nginx works for web servers
  <sub>unavailable</sub>
- **[Strale](https://strale.dev)** — 250+ quality-scored capabilities for AI agents: company data across 27 countries, compliance checks (KYB, AML, sanctions, GDPR), financial validation, web intelligence (SSL checks, DNS lookups, domain reputation), document extraction, developer tools (CVE lookup, dependency audit, code review), and data processing. Every capability independently tested with Strale Quality Score (SQS). Free tier av
  <sub>website</sub>
  <sub>`https://strale.dev`</sub>
- **[Arch Tools](https://archtools.dev)** — 53 production-ready AI tools via MCP with x402 USDC payments. Web scraping, crypto data, AI generation, OCR, and more
  <sub>website</sub>
  <sub>`https://archtools.dev`</sub>
- **[pumanitro/global-chat](https://github.com/pumanitro/global-chat)** — Cross-protocol AI agent discovery MCP server. Searchable directory of 18K+ MCP servers across 6+ registries (mcp.so, Glama, Smithery, PulseMCP), with agents.txt validation and protocol-agnostic agent search
  <sub>unavailable</sub>
- **[lazymac/k-mcp](https://github.com/lazymac2x/lazymac-k-mcp)** — Korea-focused MCP utilities for privacy compliance, KRW/BOK rates, business registration lookup, geocoding, and NLP
  <sub>JavaScript · MIT · source · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lazymac2x/lazymac-k-mcp.git`</sub>

## Frameworks

- **[FastMCP](https://github.com/PrefectHQ/fastmcp)** — A high-level framework for building MCP servers in Python
  <sub>★ 27.8k · Python · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jlowin/fastmcp.git`</sub>
- **[FastMCP](https://github.com/punkpeye/fastmcp)** — A high-level framework for building MCP servers in TypeScript
  <sub>★ 3.3k · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx fastmcp dev src/examples/addition.ts`</sub>
- **[tersePrompts/fastMCP4J](https://github.com/tersePrompts/fastMCP4J)** — Lightweight Java library for building MCP servers using annotations. Annotation-driven development with only 12 dependencies, built-in tools (memory, todo, planner, file ops, bash, telemetry), multi-class modules support, and &lt;500ms cold start
  <sub>★ 11 · Java · MIT · source · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tersePrompts/fastMCP4J.git`</sub>
- **[MervinPraison/praisonai-mcp](https://github.com/MervinPraison/praisonai-mcp)** — AI Agents framework with 64+ built-in MCP tools for automation, including search, memory, workflows, code execution, and file operations
  <sub>★ 1 · Python · MIT · uv · pushed 2026-01-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx praisonai-mcp`</sub>

## Metrics &amp; Monitoring

- **[pab1it0/prometheus-mcp-server](https://github.com/pab1it0/prometheus-mcp-server)** — A Model Context Protocol server that enables AI assistants to query and analyze Prometheus metrics through standardized interfaces
  <sub>★ 517 · Python · MIT · helm · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`helm install prometheus-mcp-server \`</sub>
- **[VictoriaMetrics-Community/mcp-victoriametrics](https://github.com/VictoriaMetrics/mcp-victoriametrics)** — The implementation of Model Context Protocol (MCP) server for VictoriaMetrics. This provides access to your VictoriaMetrics instance and seamless integration with VictoriaMetrics APIs and documentation
  <sub>★ 234 · Go · Apache-2.0 · docker · pushed 2026-08-23 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run -d --name mcp-victoriametrics \`</sub>
- **[CaesarYangs/prometheus_mcp_server](https://github.com/CaesarYangs/prometheus_mcp_server)** — A Model Context Protocol server enabling LLMs to query, analyze, and interact with Prometheus databases through predefined routes
  <sub>★ 33 · Python · MIT · npx · pushed 2025-04-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @CaesarYangs/prometheus_mcp_server --client claude`</sub>
- **[etruong42/prometheus-mcp](https://github.com/etruong42/prometheus-mcp)** — MCP server to connect LLMs with Prometheus HTTP API for metrics querying and analysis
  <sub>★ 1 · Python · MIT · source · pushed 2025-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/etruong42/prometheus-mcp.git`</sub>
- **[loginmqv/mcp-server-prometheus](https://github.com/loginmqv/mcp-server-prometheus)** — MCP server for interacting with Prometheus, enabling AI assistants to query and analyze metrics data
  <sub>unavailable</sub>
- **[Middleware MCP Server](https://github.com/middleware-labs/mcp-middleware)** — MCP server for interacting with Middleware observability data, enabling AI assistants to query logs, metrics, traces, and infrastructure telemetry through standardized interfaces
  <sub>Go · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/middleware-labs/mcp-middleware.git`</sub>

## Application Performance Monitoring

- **[dynatrace-oss/dynatrace-mcp](https://github.com/dynatrace-oss/dynatrace-mcp)** — MCP server for Dynatrace Observability monitoring, providing AI-powered insights into application performance and infrastructure health
  <sub>★ 138 · TypeScript · MIT · npx · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @dynatrace-oss/dynatrace-mcp-server@latest --help`</sub>
- **[last9/last9-mcp-server](https://github.com/last9/last9-mcp-server)** — Last9 MCP Server for observability and monitoring, providing AI assistants with access to metrics, logs, and traces
  <sub>★ 62 · Go · Apache-2.0 · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @last9/mcp-server@latest`</sub>
- **[alilxxey/openobserve-community-mcp](https://github.com/alilxxey/openobserve-community-mcp)** — MCP server for OpenObserve Community Edition via REST API. Read-only tools for searching logs, traces, stream schemas, and dashboards without requiring the Enterprise license
  <sub>★ 16 · Python · GPL-3.0 · uv · pushed 2026-03-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from openobserve-community-mcp openobserve-mcp init-config`</sub>
- **[willibrandon/CursorMCPMonitor](https://github.com/willibrandon/CursorMCPMonitor)** — #️⃣ 🏠 - Real-time monitoring tool for Model Context Protocol interactions in Cursor AI editor. Track, analyze, and debug AI context exchanges
  <sub>★ 12 · C# · MIT · docker · pushed 2025-03-12 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run -it --rm -v "$env:APPDATA\Cursor\logs:/app/logs" -e LogsRoot=/app/logs cursor-mcp-monitor`</sub>
- **[vdalhambra/siteaudit-mcp](https://github.com/vdalhambra/siteaudit-mcp)** — URL audit MCP server for SEO, performance, accessibility, and security checks
  <sub>★ 5 · Python · MIT · npx · pushed 2026-04-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @vdalhambra/siteaudit --client claude`</sub>
- **[AlexlaGuardia/Vigil](https://github.com/AlexlaGuardia/Vigil)** — /🏠 - MCPWatch instruments any Python MCP server in one line — FastMCP and low-level Server, same API. Per-tool latency (p50/p95/p99), error rates, silent-failure detection, and call-volume tracking. REST API, CLI, alerts. MIT
  <sub>★ 1 · Python · MIT · pip · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install vigil-agent`</sub>
- **[unitedideas/resolve-mcp](https://github.com/unitedideas/resolve-mcp)** — Structured error recovery for AI agents. Returns resolution playbooks with backoff schedules, retry strategies, and recovery steps for 20+ services (OpenAI, Anthropic, Stripe, AWS, Postgres, Redis, Twilio, etc.). Complements monitoring tools by telling agents how to recover from errors, not just detect them
  <sub>★ 1 · Python · MIT · uv · pushed 2026-03-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx resolve-mcp`</sub>
- **[ingero-io/ingero](https://github.com/ingero-io/ingero)** — eBPF-based GPU causal observability agent with MCP server, providing AI assistants with causal chains explaining GPU latency from CUDA Runtime/Driver API tracing and host kernel event tracing
  <sub>unavailable</sub>
- **[Polar Signals Remote MCP](https://www.polarsignals.com/blog/posts/2025/07/17/the-mcp-for-performance-engineering)** — MCP server for Polar Signals Cloud continuous profiling platform, enabling AI assistants to analyze CPU performance, memory usage, and identify optimization opportunities in production systems
  <sub>website</sub>
  <sub>`https://www.polarsignals.com/blog/posts/2025/07/17/the-mcp-for-performance-engineering`</sub>
- **[Uptrack-App/uptrack-mcp](https://github.com/Uptrack-App/uptrack-mcp)** — Uptime monitoring MCP server. 10 tools for listing/creating/pausing monitors and acknowledging incidents. Remote Streamable-HTTP at api.uptrack.app/mcp (OAuth 2.0) or stdio via npx @uptrack-app/mcp
  <sub>JavaScript · source · pushed 2026-05-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Uptrack-App/uptrack-mcp.git`</sub>
- **[nicofains1/agentwatch](https://github.com/nicofains1/agentwatch)** — Multi-agent observability for cascade failure detection, fleet-wide heartbeat monitoring, and forensic replay. Works as an npm library or MCP server
  <sub>TypeScript · MIT · npx · pushed 2026-04-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @nicofains1/agentwatch demo`</sub>
- **[kame6493-del/mcp-diagnostics](https://github.com/kame6493-del/mcp-diagnostics)** — Website and server diagnostics MCP server for DNS, SSL, HTTP headers, security audits, WHOIS, and tech-stack detection
  <sub>JavaScript · source · pushed 2026-04-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kame6493-del/mcp-diagnostics.git`</sub>
- **[Voidly](https://github.com/voidly-ai/mcp-server)** — MCP server for global network and censorship intelligence, useful for service-accessibility monitoring and blocking diagnostics
  <sub>unavailable</sub>

## Alerting &amp; Notification

- **[kaznak/alertmanager-mcp](https://github.com/kaznak/alertmanager-mcp)** — A Model Context Protocol server that integrates with Prometheus Alertmanager for alert management and notification
  <sub>★ 10 · TypeScript · MIT · npm · pushed 2025-03-28 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g alertmanager-mcp`</sub>

## Social Media Monitoring

- **[Xquik](https://xquik.com)** — X/Twitter account monitoring and data extraction — MCP server, REST API, HMAC webhooks, 40+ extraction tools
  <sub>website</sub>
  <sub>`https://xquik.com`</sub>

## Related Resources

- **[awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers/)** — A comprehensive list of all MCP servers
  <sub>★ 95.4k · MIT · npx · pushed 2026-09-21 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npx awesome-mcp search postgres`</sub>
- **[awesome-mcp-clients](https://github.com/punkpeye/awesome-mcp-clients/)** — A list of MCP clients
  <sub>★ 6.6k · MIT · source · pushed 2026-06-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/punkpeye/awesome-mcp-clients/.git`</sub>
- **[awesome](https://github.com/sindresorhus/awesome#readme)** — Awesome lists about all kinds of interesting topics
  <sub>CC0-1.0 · in-repo · pushed 2026-09-02</sub>
  <sub>`git clone https://github.com/sindresorhus/awesome.git && cd awesome/#readme`</sub>

## Memory &amp; Context

- **[vectorize-io/hindsight](https://github.com/vectorize-io/hindsight)** — Long-term memory for AI agents with semantic search, auto-capture, and framework integrations
  <sub>★ 24.6k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @vectorize-io/hindsight-coding-agents install all # every detected agent, wired natively`</sub>
- **[mcpware/claude-code-organizer](https://github.com/mcpware/cross-code-organizer)** — MCP server to organize Claude Code configurations — scan, move, delete memories, skills, MCP servers, and hooks across project and user scopes
  <sub>★ 379 · JavaScript · MIT · npx · pushed 2026-09-13 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx @mcpware/cross-code-organizer --distill <session.jsonl>`</sub>
- **[qualixar/superlocalmemory](https://github.com/qualixar/superlocalmemory)** — Local-first persistent agent memory with hybrid retrieval across semantic, lexical, temporal, and graph signals
  <sub>★ 225 · Python · AGPL-3.0 · npm · pushed 2026-09-12 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npm install -g superlocalmemory`</sub>
- **[omega-memory/omega-memory](https://github.com/omega-memory/omega-memory)** — Local-first persistent memory for AI agents. SQLite + ONNX embeddings, semantic search, auto-capture, checkpoint/resume. #1 on LongMemEval benchmark
  <sub>★ 217 · Python · Apache-2.0 · pip · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install omega-memory[server] # Full install (memory + MCP server)`</sub>
- **[novyxlabs/novyx-mcp](https://github.com/novyxlabs/novyx-mcp)** — Persistent memory and governance for AI agents with local core memory and optional cloud-backed policy, approval, and audit workflows
  <sub>★ 30 · Python · MIT · pip · pushed 2026-07-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install novyx-mcp`</sub>
- **[dakera-ai/dakera-mcp](https://github.com/Dakera-AI/dakera-mcp)** — Self-hosted MCP-native agent memory server. 83 tools for persistent, decay-weighted episodic memory across sessions. RocksDB + HNSW, 87.8% LoCoMo benchmark. Docker Compose deployment, multi-SDK support
  <sub>★ 8 · Rust · npm · pushed 2026-09-14 · macOS</sub>
  <sub>`npm install -g @dakera-ai/dakera-mcp`</sub>
- **[SKULLFIRE07/cortex-memory](https://github.com/SKULLFIRE07/cortex-memory)** — Persistent AI memory for coding assistants. Auto-captures decisions, patterns, and context across sessions. VSCode extension + CLI + MCP server. MIT licensed
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-03-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g cortex-memory`</sub>
- **[eidetic-works/nucleus-mcp](https://github.com/eidetic-works/nucleus-mcp)** — Persistent memory and execution context MCP server for AI IDEs, with local-first project memory and governance tools
  <sub>unavailable</sub>

## Project Management

- **[sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian)** — MCP server for Atlassian products (Confluence and Jira). Supports Confluence Cloud, Jira Cloud, and Jira Server/Data Center. Provides comprehensive tools for searching, reading, creating, and managing content across Atlassian workspaces
  <sub>★ 5.9k · Python · MIT · uv · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-atlassian`</sub>
- **[nguyenvanduocit/jira-mcp](https://github.com/nguyenvanduocit/jira-mcp)** — A Go-based MCP connector for Jira that enables AI assistants like Claude to interact with Atlassian Jira. This tool provides a seamless interface for AI models to perform common Jira operations including issue management, sprint planning, and workflow transitions
  <sub>★ 97 · Go · MIT · go · pushed 2026-04-18 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/nguyenvanduocit/jira-mcp/cmd/jira-cli@latest`</sub>
- **[Pangu-Immortal/qflow](https://github.com/Pangu-Immortal/qflow)** — AI project-management MCP server for task tracking, spec-driven development, multi-agent collaboration, quality gates, and workflow automation
  <sub>★ 9 · TypeScript · MIT · clone · pushed 2026-04-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Pangu-Immortal/qflow.git`</sub>

## Ticketing Systems

- **[effytech/freshdesk-mcp](https://github.com/effytech/freshdesk_mcp)** — MCP server that integrates with Freshdesk, enabling AI models to interact with Freshdesk modules and perform various support operations
  <sub>★ 68 · Python · MIT · npx · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @effytech/freshdesk_mcp --client claude`</sub>
- **[dbsanfte/topdesk-mcp](https://github.com/dbsanfte/topdesk-mcp)** — MCP server for the Topdesk ticketing system, allowing AI models to interact with and add comments to incident tickets
  <sub>★ 3 · Python · MIT · source · pushed 2025-07-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dbsanfte/topdesk-mcp.git`</sub>

## CMS &amp; Web Platforms

- **[mvtandas/wp-cli-mcp](https://github.com/mvtandas/wp-cli-mcp)** — WordPress management MCP server built on WP-CLI for themes, plugins, posts, menus, users, database operations, and scaffolding
  <sub>★ 5 · JavaScript · MIT · npm · pushed 2026-04-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g wp-cli-mcp`</sub>

## API Cost Management

- **[benbencodes/llm-prices](https://github.com/benbencodes/llm-prices)** — Zero-dependency Python CLI, library, and MCP server for calculating and comparing LLM API costs across major providers
  <sub>★ 1 · Python · MIT · pipx · pushed 2026-05-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install git+https://github.com/benbencodes/llm-prices`</sub>


---

Snapshot 2026-09-21. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
