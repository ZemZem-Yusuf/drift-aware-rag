# Golden set review

For each question below:

1. Read the **question**: would a real user ask this? Is it clear and about Kubernetes v1.33?
2. Read the **documentation excerpts**: do they really answer the question? Is an obviously
   better section missing?
3. Read the **reference answer**: is it correct *according to the excerpts*?
4. Tick **exactly one** box (replace `[ ]` with `[x]`). If you pick *Needs changes*, write what
   to change under **Notes**.

**Out-of-scope questions** are tests that the system *refuses* to answer. If the question really
is outside the Kubernetes docs, tick **Correct as written** (it stays in the set as a refusal
test). Tick **Reject** only if it should be removed from the set.

When done, run: `uv run driftrag-golden apply --reviewer "Your Name"`

---

### `job-completions`

**Question** (en, task): How do I run a batch job that must succeed 5 times, requesting 2 pods at a time?

**Reference answer:** Set `completions: 5` and `parallelism: 2` in the Job spec. The actual parallelism can be more or less than requested.

**Relevant documentation:**
- `concepts/workloads/controllers/job.md`, section: *Jobs > Writing a Job spec*
  > [Jobs > Writing a Job spec]
  > As with all other Kubernetes config, a Job needs `apiVersion`, `kind`, and `metadata` fields.
  > When the control plane creates new Pods for a Job, the `.metadata.name` of the
  > Job is part of the basis for naming those Pods. The name of a Job must be a valid
  > DNS subdomain
  > value, but this can produce unexpected results for the Pod hostnames. For best compatibility,
  > the name should follow the more restrictive rules for a
  > DNS label.
  > Even when the name is a DNS subdomain, the name must be no longer than 63
  > characters.
  > A Job also needs a `.spec` section.
  > [Jobs > Writing a Job spec > Job Labels]
  > Job labels will have `batch.kubernetes.io/` prefix for `job-name` and `controller-uid`.
  > [Jobs > Writing a Job spec > Pod Template]
  > The `.spec.template` is the only required field of the `.spec`.
  > The `.spec.template` is a pod template.
  > It has exactly the same schema as a Pod,
  > except it is nested and does not have an `apiVersion` or `kind`.
  > In addition to required fields for a Pod, a pod template in a Job must specify appropriate
  > labels (see pod selector) and an appropriate restart policy.
  > Only a `RestartPolicy`
  > equal to `Never` or `OnFailure` is allowed.
  > [Jobs > Writing a Job spec > Pod selector]
  > The `.spec.selector` field is optional. In almost all cases you should not specify it.
  > See section specifying your own pod selector.
  > [Jobs > Writing a Job spec > Parallel execution for Jobs {#parallel-jobs}]
  > There are three main types of task suitable to run as a Job:
  > 1. Non-parallel Jobs
  >    - normally, only one Pod is started, unless the Pod fails.
  >    - the Job is complete as soon as its Pod terminates successfully.
  > 1. Parallel Jobs with a *fixed completion count*:
  >    - specify a non-zero positive value for `.spec.completions`.
  >    - the Job represents the overall task, and is complete when there are `.spec.completions` successful Pods.
  >    - when using `.spec.completionMode="Indexed"`, each Pod gets a different index in the range 0 to `.spec.completions-1`.
  > 1. Parallel Jobs with a *work queue*:
  >    - do not specify `.spec.completions`, default to `.spec.parallelism`.
  >    - the Pods must coordinate amongst themselves or an external service to determine
  >      what each should work on. For example, a Pod might fetch a batch of up to N items from the work queue.
  >    - each Pod is independently capable of determining whether or not all its peers are done,
  >      and thus that the entire Job is done.
  >    - when _any_ Pod from the Job terminates with success, no new Pods are created.
  >    - once at least one Pod has terminated with success and all Pods are terminated,
  >      then the Job is completed with success.
  >    - once any Pod has exited with success, no other Pod should still be doing any work
  >      for this task or writing any output. They should all be in the process of exiting.
  > For a _non-parallel_ Job, you can leave both `.spec.completions` and `.spec.parallelism` unset.
  > When both are unset, both are defaulted to 1.
  > For a _fixed completion count_ Job, you should set `.spec.completions` to the number of completions needed.
  > You can set `.spec.parallelism`, or leave it unset and it will default to 1.
  > For a _work queue_ Job, you must leave `.spec.completions` unset, and set `.spec.parallelism` to
  > a non-negative integer.
  > For more information about how to make use of the different types of job,
  > see the job patterns section.
  > [Jobs > Writing a Job spec > Parallel execution for Jobs {#parallel-jobs} > Controlling parallelism]
  > The requested parallelism (`.spec.parallelism`) can be set to any non-negative value.
  > If it is unspecified, it defaults to 1.
  > If it is specified as 0, then the Job is effectively paused until it is increased.
  > Actual parallelism (number of pods running at any instant) may be more or less than requested
  > parallelism, for a variety of reasons:
  > - For _fixed completion count_ Jobs, the actual number of pods running in parallel will not exceed the number of
  >   remaining completions. Higher values of `.spec.parallelism` are effectively ignored.
  > - For _work queue_ Jobs, no new Pods are started after any Pod has succeeded -- remaining Pods are allowed to complete, however.
  > - If the Job  has not had time to react.
  > - If the Job controller failed to create Pods for any reason (lack of `ResourceQuota`, lack of permission, etc.),
  >   then there may be fewer pods than requested.
  > - The Job controller may throttle new Pod creation due to excessive previous pod failures in the same Job.
  > - When a Pod is gracefully shut down, it takes time to stop.
  > [Jobs > Writing a Job spec > Completion mode]
  > Jobs with _fixed completion count_ - that is, jobs that have non null
  > `.spec.completions` - can have a completion mode that is specified in `.spec.completionMode`:
  > - `NonIndexed` (default): the Job is considered complete when there have been
  >   `.spec.completions` successfully completed Pods. In other words, each Pod
  >   completion is homologous to each other. Note that Jobs that have null
  >   `.spec.completions` are implicitly `NonIndexed`.
  > - `Indexed`: the Pods of a Job get an associated completion index from 0 to
  >   `.spec.completions-1`. The index is available through four mechanisms:
  >   - The Pod annotation `batch.kubernetes.io/job-completion-index`.
  >   - The Pod label `batch.kubernetes.io/job-completion-index` (for v1.28 and later). Note
  >     the feature gate `PodIndexLabel` must be enabled to use this label, and it is enabled
  >     by default.
  >   - As part of the Pod hostname, following the pattern `$(job-name)-$(index)`.
  >     When you use an Indexed Job in combination with a
  >     , Pods within the Job can use
  >     the deterministic hostnames to address each other via DNS. For more information about
  >     how to configure this, see Job with Pod-to-Pod Communication.
  >   - From the containerized task, in the environment variable `JOB_COMPLETION_INDEX`.
  >   The Job is considered complete when there is one successfully completed Pod
  >   for each index. For more information about how to use this mode, see
  >   Indexed Job for … (section continues)

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 4 (Youssef Zemzem, 2026-11-07): parallelism described as requested, not guaranteed

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `job-ttl`

**Question** (en, task): How do I have finished Jobs deleted automatically?

**Reference answer:** Set `ttlSecondsAfterFinished` on the Job. The TTL controller makes it eligible for deletion after that many seconds and deletes the Job and its dependent Pods.

**Relevant documentation:**
- `concepts/workloads/controllers/job.md`, section: *Jobs > Clean up finished jobs automatically*
  > [Jobs > Clean up finished jobs automatically]
  > Finished Jobs are usually no longer needed in the system. Keeping them around in
  > the system will put pressure on the API server. If the Jobs are managed directly
  > by a higher level controller, such as
  > CronJobs, the Jobs can be
  > cleaned up by CronJobs based on the specified capacity-based cleanup policy.
  > [Jobs > Clean up finished jobs automatically > TTL mechanism for finished Jobs]
  > Another way to clean up finished Jobs (either `Complete` or `Failed`)
  > automatically is to use a TTL mechanism provided by a
  > TTL controller for
  > finished resources, by specifying the `.spec.ttlSecondsAfterFinished` field of
  > the Job.
  > When the TTL controller cleans up the Job, it will delete the Job cascadingly,
  > i.e. delete its dependent objects, such as Pods, together with the Job. Note
  > that when the Job is deleted, its lifecycle guarantees, such as finalizers, will
  > be honored.
  > For example:
  > ```yaml
  > apiVersion: batch/v1
  > kind: Job
  > metadata:
  >   name: pi-with-ttl
  > spec:
  >   ttlSecondsAfterFinished: 100
  >   template:
  >     spec:
  >       containers:
  >       - name: pi
  >         image: perl:5.34.0
  >         command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"]
  >       restartPolicy: Never
  > ```
  > The Job `pi-with-ttl` will be eligible to be automatically deleted, `100`
  > seconds after it finishes.
  > If the field is set to `0`, the Job will be eligible to be automatically deleted
  > immediately after it finishes. If the field is unset, this Job won't be cleaned
  > up by the TTL controller after it finishes.
  > It is recommended to set `ttlSecondsAfterFinished` field because unmanaged jobs
  > (Jobs that you created directly, and not indirectly through other workload APIs
  > such as CronJob) have a default deletion
  > policy of `orphanDependents` causing Pods created by an unmanaged Job to be left around
  > after that Job is fully deleted.
  > Even though the control plane eventually
  > garbage collects
  > the Pods from a deleted Job after they either fail or complete, sometimes those
  > lingering pods may cause cluster performance degradation or in worst case cause the
  > cluster to go offline due to this degradation.
  > You can use LimitRanges and
  > ResourceQuotas to place a
  > cap on the amount of resources that a particular namespace can
  > consume.

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 4 (Youssef Zemzem, 2026-11-07): reviewer's wording: eligible for deletion after the TTL

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `default-storageclass`

**Question** (en, concept): What happens when a PersistentVolumeClaim doesn't name a storage class?

**Reference answer:** If the cluster has a default StorageClass, it's assigned to the claim. A volume is then provisioned dynamically only if dynamic provisioning is enabled, including the DefaultStorageClass admission controller.

**Relevant documentation:**
- `concepts/storage/storage-classes.md`, section: *Storage Classes > Default StorageClass*
  > [Storage Classes > Default StorageClass]
  > You can mark a StorageClass as the default for your cluster.
  > For instructions on setting the default StorageClass, see
  > Change the default StorageClass.
  > When a PVC does not specify a `storageClassName`, the default StorageClass is
  > used.
  > If you set the
  > `storageclass.kubernetes.io/is-default-class`
  > annotation to true on more than one StorageClass in your cluster, and you then
  > create a PersistentVolumeClaim with no `storageClassName` set, Kubernetes
  > uses the most recently created default StorageClass.
  > You should try to only have one StorageClass in your cluster that is
  > marked as the default. The reason that Kubernetes allows you to have
  > multiple default StorageClasses is to allow for seamless migration.
  > You can create a PersistentVolumeClaim without specifying a `storageClassName`
  > for the new PVC, and you can do so even when no default StorageClass exists
  > in your cluster. In this case, the new PVC creates as you defined it, and the
  > `storageClassName` of that PVC remains unset until a default becomes available.
  > You can have a cluster without any default StorageClass. If you don't mark any
  > StorageClass as default (and one hasn't been set for you by, for example, a cloud provider),
  > then Kubernetes cannot apply that defaulting for PersistentVolumeClaims that need
  > it.
  > If or when a default StorageClass becomes available, the control plane identifies any
  > existing PVCs without `storageClassName`. For the PVCs that either have an empty
  > value for `storageClassName` or do not have this key, the control plane then
  > updates those PVCs to set `storageClassName` to match the new default StorageClass.
  > If you have an existing PVC where the `storageClassName` is `""`, and you configure
  > a default StorageClass, then this PVC will not get updated.
  > In order to keep binding to PVs with `storageClassName` set to `""`
  > (while a default StorageClass is present), you need to set the `storageClassName`
  > of the associated PVC to `""`.
- `concepts/storage/dynamic-provisioning.md`, section: *Dynamic Volume Provisioning > Defaulting Behavior*
  > [Dynamic Volume Provisioning > Defaulting Behavior]
  > Dynamic provisioning can be enabled on a cluster such that all claims are
  > dynamically provisioned if no storage class is specified. A cluster administrator
  > can enable this behavior by:
  > - Marking one `StorageClass` object as *default*;
  > - Making sure that the `DefaultStorageClass` admission controller
  >   is enabled on the API server.
  > An administrator can mark a specific `StorageClass` as default by adding the
  > `storageclass.kubernetes.io/is-default-class` annotation to it.
  > When a default `StorageClass` exists in a cluster and a user creates a
  > `PersistentVolumeClaim` with `storageClassName` unspecified, the
  > `DefaultStorageClass` admission controller automatically adds the
  > `storageClassName` field pointing to the default storage class.
  > Note that if you set the `storageclass.kubernetes.io/is-default-class`
  > annotation to true on more than one StorageClass in your cluster, and you then
  > create a `PersistentVolumeClaim` with no `storageClassName` set, Kubernetes
  > uses the most recently created default StorageClass.

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 4 (Youssef Zemzem, 2026-11-07): default class assignment distinguished from the conditions for dynamic provisioning

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `priority-preemption`

**Question** (en, concept): How can important pods push out less important ones when the cluster is full?

**Reference answer:** Create a PriorityClass and set `priorityClassName` on the important Pods; when they can't be scheduled, the scheduler can preempt (evict) lower-priority Pods.

**Relevant documentation:**
- `concepts/scheduling-eviction/pod-priority-preemption.md`, section: *Pod Priority and Preemption > How to use priority and preemption*
  > [Pod Priority and Preemption > How to use priority and preemption]
  > To use priority and preemption:
  > 1.  Add one or more PriorityClasses.
  > 1.  Create Pods with`priorityClassName` set to one of the added
  >     PriorityClasses. Of course you do not need to create the Pods directly;
  >     normally you would add `priorityClassName` to the Pod template of a
  >     collection object like a Deployment.
  > Keep reading for more information about these steps.
  > Kubernetes already ships with two PriorityClasses:
  > `system-cluster-critical` and `system-node-critical`.
  > These are common classes and are used to ensure that critical components are always scheduled first.
- `concepts/scheduling-eviction/pod-priority-preemption.md`, section: *Pod Priority and Preemption > PriorityClass*
  > [Pod Priority and Preemption > PriorityClass]
  > A PriorityClass is a non-namespaced object that defines a mapping from a
  > priority class name to the integer value of the priority. The name is specified
  > in the `name` field of the PriorityClass object's metadata. The value is
  > specified in the required `value` field. The higher the value, the higher the
  > priority.
  > The name of a PriorityClass object must be a valid
  > DNS subdomain name,
  > and it cannot be prefixed with `system-`.
  > A PriorityClass object can have any 32-bit integer value smaller than or equal
  > to 1 billion. This means that the range of values for a PriorityClass object is
  > from -2147483648 to 1000000000 inclusive. Larger numbers are reserved for
  > built-in PriorityClasses that represent critical system Pods. A cluster
  > admin should create one PriorityClass object for each such mapping that they want.
  > PriorityClass also has two optional fields: `globalDefault` and `description`.
  > The `globalDefault` field indicates that the value of this PriorityClass should
  > be used for Pods without a `priorityClassName`. Only one PriorityClass with
  > `globalDefault` set to true can exist in the system. If there is no
  > PriorityClass with `globalDefault` set, the priority of Pods with no
  > `priorityClassName` is zero.
  > The `description` field is an arbitrary string. It is meant to tell users of the
  > cluster when they should use this PriorityClass.
  > [Pod Priority and Preemption > PriorityClass > Notes about PodPriority and existing clusters]
  > -   If you upgrade an existing cluster without this feature, the priority
  >     of your existing Pods is effectively zero.
  > -   Addition of a PriorityClass with `globalDefault` set to `true` does not
  >     change the priorities of existing Pods. The value of such a PriorityClass is
  >     used only for Pods created after the PriorityClass is added.
  > -   If you delete a PriorityClass, existing Pods that use the name of the
  >     deleted PriorityClass remain unchanged, but you cannot create more Pods that
  >     use the name of the deleted PriorityClass.
  > [Pod Priority and Preemption > PriorityClass > Example PriorityClass]
  > ```yaml
  > apiVersion: scheduling.k8s.io/v1
  > kind: PriorityClass
  > metadata:
  >   name: high-priority
  > value: 1000000
  > globalDefault: false
  > description: "This priority class should be used for XYZ service pods only."
  > ```
- `concepts/scheduling-eviction/pod-priority-preemption.md`, section: *Pod Priority and Preemption > Preemption*
  > [Pod Priority and Preemption > Preemption]
  > When Pods are created, they go to a queue and wait to be scheduled. The
  > scheduler picks a Pod from the queue and tries to schedule it on a Node. If no
  > Node is found that satisfies all the specified requirements of the Pod,
  > preemption logic is triggered for the pending Pod. Let's call the pending Pod P.
  > Preemption logic tries to find a Node where removal of one or more Pods with
  > lower priority than P would enable P to be scheduled on that Node. If such a
  > Node is found, one or more lower priority Pods get evicted from the Node. After
  > the Pods are gone, P can be scheduled on the Node.
  > [Pod Priority and Preemption > Preemption > User exposed information]
  > When Pod P preempts one or more Pods on Node N, `nominatedNodeName` field of Pod
  > P's status is set to the name of Node N. This field helps the scheduler track
  > resources reserved for Pod P and also gives users information about preemptions
  > in their clusters.
  > Please note that Pod P is not necessarily scheduled to the "nominated Node".
  > The scheduler always tries the "nominated Node" before iterating over any other nodes.
  > After victim Pods are preempted, they get their graceful termination period. If
  > another node becomes available while scheduler is waiting for the victim Pods to
  > terminate, scheduler may use the other node to schedule Pod P. As a result
  > `nominatedNodeName` and `nodeName` of Pod spec are not always the same. Also, if
  > the scheduler preempts Pods on Node N, but then a higher priority Pod than Pod P
  > arrives, the scheduler may give Node N to the new higher priority Pod. In such a
  > case, scheduler clears `nominatedNodeName` of Pod P. By doing this, scheduler
  > makes Pod P eligible to preempt Pods on another Node.
  > [Pod Priority and Preemption > Preemption > Limitations of preemption > Graceful termination of preemption victims]
  > When Pods are preempted, the victims get their
  > graceful termination period.
  > They have that much time to finish their work and exit. If they don't, they are
  > killed. This graceful termination period creates a time gap between the point
  > that the scheduler preempts Pods and the time when the pending Pod (P) can be
  > scheduled on the Node (N). In the meantime, the scheduler keeps scheduling other
  > pending Pods. As victims exit or get terminated, the scheduler tries to schedule
  > Pods in the pending queue. Therefore, there is usually a time gap between the
  > point that scheduler preempts victims and the time that Pod P is scheduled. In
  > order to minimize this gap, one can set graceful termination period of lower
  > priority Pods to zero or a small number.
  > [Pod Priority and Preemption > Preemption > Limitations of preemption > PodDisruptionBudget is supported, but not guaranteed]
  > A PodDisruptionBudget (PDB)
  > allows application owners to limit the number of Pods of a replicated application
  > that are down simultaneously from voluntary disruptions. Kubernetes supports
  > PDB when preempting Pods, but respecting PDB is best effort. The scheduler tries
  > to find victims whose PDB are not violated by preemption, but if no such victims
  > are found, preemption will still happen, and lower priority Pods will be removed
  > despite their PDBs being violated.
  > [Pod Priority and Preemption > Preemption > Limitations of preemption > Inter-Pod affinity on lower-priority Pods]
  > A Node is considered for preemption only when the answer to this question is
  > yes: "If all the Pods with lower priority than the pending Pod are removed from
  > the Node, can the pending Pod be scheduled on the Node?"
  > Preemption does not necessarily remove all lower-priority
  > Pods. If the pending Pod can be scheduled by removing fewer than all
  > lower-priority Pods, then only a portion of the lower-priority Pods are removed.
  > Even so, the answer to the preceding question must be yes. If the answer is no,
  > the Node is not considered for preemption.
  > If a pending Pod has inter-pod affinity
  > to one or more of the lower-priority Pods on the Node, the inter-Pod affinity
  > rule cannot be satisfied in the absence of those lower-priority Pods. In this case,
  > the scheduler does not preempt any Pods on the Node. Instead, it looks for another
  > Node. The scheduler might find a suitable Node or it might not. There is no
  > guarantee that the pending Pod can be scheduled.
  > Our recommended solution for this problem is to create inter-Pod affinity only
  > towards equal or higher priority Pods.
  > [Pod Priority and Preemption > Preemption > Limitations of preemption > Cross node preemption]
  > Suppose a Node N is being considered for preemption so that a pending Pod P can
  > be scheduled on N. P might become feasible on N only if a Pod on another Node is
  > preempted. Here's an example:
  > *   Pod P is being considered for Node N.
  > *   Pod Q is running on another Node in the same Zone as Node N.
  > *   Pod P has Zone-wide anti-affinity with Pod Q (`topologyKey:
  >     topology.kubernetes.io/zone`).
  > *   There are no other cases of anti-affinity between Pod P and other Pods in
  >     the Zone.
  > *   In order to schedule Pod P on Node N, Pod Q can be preempted, but scheduler
  >     does not perform cross-node preemption. So, Pod P will be deemed
  >     unschedulable on Node N.
  > If Pod Q were removed from its Node, the Pod anti-affinity violation would be
  > gone, and Pod P could possibly be scheduled on Node N.
  > We may consider adding cross Node preemption in future versions if there is
  > enough demand and if we find an algorithm with reasonable performance.

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 4 (Youssef Zemzem, 2026-11-07): added the section that documents priorityClassName

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `sidecar-vs-init`

**Question** (en, concept): What is a sidecar container and how is it different from an init container?

**Reference answer:** Sidecar containers run alongside the app containers and stay running for the Pod's lifetime; init containers run to completion before the app containers start.

**Relevant documentation:**
- `concepts/workloads/pods/sidecar-containers.md`, section: *Sidecar Containers > Differences from init containers*
  > [Sidecar Containers > Differences from init containers]
  > Sidecar containers work alongside the main container, extending its functionality and
  > providing additional services.
  > Sidecar containers run concurrently with the main application container. They are active
  > throughout the lifecycle of the pod and can be started and stopped independently of the
  > main container. Unlike init containers,
  > sidecar containers support probes to control their lifecycle.
  > Sidecar containers can interact directly with the main application containers, because
  > like init containers they always share the same network, and can optionally also share
  > volumes (filesystems).
  > Init containers stop before the main containers start up, so init containers cannot
  > exchange messages with the app container in a Pod. Any data passing is one-way
  > (for example, an init container can put information inside an `emptyDir` volume).
  > Changing the image of a sidecar container will not cause the Pod to restart, but will
  > trigger a container restart.

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 4 (Youssef Zemzem, 2026-11-07): removed the unsupported start-order claim for sidecars

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `control-plane-components`

**Question** (en, concept): What does each part of the Kubernetes control plane do?

**Reference answer:** kube-apiserver exposes the API, etcd stores cluster data, kube-scheduler assigns Pods to nodes, kube-controller-manager runs the controllers, and the optional cloud-controller-manager integrates with a cloud provider. Nodes run the kubelet and a container runtime, and optionally kube-proxy.

**Relevant documentation:**
- `concepts/overview/components.md`, section: *Kubernetes Components > Core Components*
  > [Kubernetes Components > Core Components]
  > A Kubernetes cluster consists of a control plane and one or more worker nodes.
  > Here's a brief overview of the main components:
  > [Kubernetes Components > Core Components > Control Plane Components]
  > Manage the overall state of the cluster:
  > kube-apiserver
  > : The core component server that exposes the Kubernetes HTTP API.
  > etcd
  > : Consistent and highly-available key value store for all API server data.
  > kube-scheduler
  > : Looks for Pods not yet bound to a node, and assigns each Pod to a suitable node.
  > kube-controller-manager
  > : Runs controllers to implement Kubernetes API behavior.
  > cloud-controller-manager (optional)
  > : Integrates with underlying cloud provider(s).
  > [Kubernetes Components > Core Components > Node Components]
  > Run on every node, maintaining running pods and providing the Kubernetes runtime environment:
  > kubelet
  > : Ensures that Pods are running, including their containers.
  > kube-proxy (optional)
  > : Maintains network rules on nodes to implement Services.
  > Container runtime
  > : Software responsible for running containers. Read
  >   Container Runtimes to learn more.
  > Your cluster may require additional software on each node; for example, you might also
  > run systemd on a Linux node to supervise local components.

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 4 (Youssef Zemzem, 2026-11-07): added cloud-controller-manager; kube-proxy described as optional

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-private-registry`

**Question** (fr, task): Comment utiliser une image d'un registre privé qui demande une authentification ?

**Reference answer:** Créer un Secret de type docker-registry (par ex. `regcred`) et le référencer dans `imagePullSecrets` du Pod.

**Relevant documentation:**
- `tasks/configure-pod-container/pull-image-private-registry.md`, section: *Récupération d'une image d'un registre privé > Créez un Secret en fournissant les identifiants sur la ligne de commande*
  > [Récupération d'une image d'un registre privé > Créez un Secret en fournissant les identifiants sur la ligne de commande]
  > Créez ce secret, en le nommant `regcred` :
  > ```shell
  > kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
  > ```
  > où :
  > * `<your-registry-server>` est votre FQDN de registre de docker privé. (https://index.docker.io/v1/ for DockerHub)
  > * `<your-name>` est votre nom d'utilisateur Docker.
  > * `<your-pword>` est votre mot de passe Docker.
  > * `<your-email>` est votre email Docker.
  > Vous avez réussi à définir vos identifiants Docker dans le cluster comme un secret appelé `regcred`.
  > Saisir des secrets sur la ligne de commande peut les conserver dans l'historique de votre shell sans protection, et ces secrets peuvent également être visibles par d'autres utilisateurs sur votre ordinateur pendant l'exécution de `kubectl`.
- `tasks/configure-pod-container/pull-image-private-registry.md`, section: *Récupération d'une image d'un registre privé > Créez un Pod qui utilise votre Secret*
  > [Récupération d'une image d'un registre privé > Créez un Pod qui utilise votre Secret]
  > Voici un fichier de configuration pour un Pod qui a besoin d'accéder à vos identifiants Docker dans `regcred` :
  > Example file `pods/private-reg-pod.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: private-reg
  > spec:
  >   containers:
  >   - name: private-reg-container
  >     image: <your-private-image>
  >   imagePullSecrets:
  >   - name: regcred
  > ```
  > Téléchargez le fichier ci-dessus :
  > ```shell
  > wget -O my-private-reg-pod.yaml https://k8s.io/examples/pods/private-reg-pod.yaml
  > ```
  > Dans le fichier `my-private-reg-pod.yaml`, remplacez `<your-private-image>` par le chemin d'accès à une image dans un registre privé tel que
  > ```none
  > your.private.registry.example.com/janedoe/jdoe-private:v1
  > ```
  > Pour récupérer l'image du registre privé, Kubernetes a besoin des identifiants.
  > Le champ `imagePullSecrets` dans le fichier de configuration spécifie que Kubernetes doit obtenir les informations d'identification d'un Secret nommé `regcred`.
  > Créez un Pod qui utilise votre secret et vérifiez que le Pod est bien lancé :
  > ```shell
  > kubectl apply -f my-private-reg-pod.yaml
  > kubectl get pod private-reg
  > ```
  > ##
  > ##
  > * Pour en savoir plus sur les Secrets.
  > * Pour en savoir plus sur l'utilisation d'un registre privé.
  > * Pour en savoir plus sur l'ajout d'un imagePullSecrets à un compte de service.
  > * Voir kubectl crée un Secret de registre de docker.
  > * Voir Secret.
  > * Voir le champ `imagePullSecrets` de PodSpec.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-emptydir`

**Question** (fr, task): Comment donner à un Pod un volume temporaire qui disparaît avec lui ?

**Reference answer:** Utiliser un volume `emptyDir`, qui existe tant que le Pod tourne sur le nœud.

**Relevant documentation:**
- `tasks/configure-pod-container/configure-volume-storage.md`, section: *Configurer un pod en utilisant un volume pour le stockage > Configurer un volume pour un Pod*
  > [Configurer un pod en utilisant un volume pour le stockage > Configurer un volume pour un Pod]
  > Dans cet exercice, vous créez un pod qui contient un seul conteneur. Ce Pod a un Volume de type
  > emptyDir qui dure toute la vie du Pod, même si le conteneur se termine et redémarre.
  > Voici le fichier de configuration du Pod :
  > Example file `pods/storage/redis.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: redis
  > spec:
  >   containers:
  >   - name: redis
  >     image: redis
  >     volumeMounts:
  >     - name: redis-storage
  >       mountPath: /data/redis
  >   volumes:
  >   - name: redis-storage
  >     emptyDir: {}
  > ```
  > 1. Créez le Pod :
  >     ```shell
  >     kubectl apply -f https://k8s.io/examples/pods/storage/redis.yaml
  >     ```
  > 1. Vérifiez que le conteneur du pod est en cours d'exécution, puis surveillez les modifications apportées au pod :
  >     ```shell
  >     kubectl get pod redis --watch
  >     ```
  >     La sortie ressemble à ceci :
  >     ```console
  >     NAME      READY     STATUS    RESTARTS   AGE
  >     redis     1/1       Running   0          13s
  >     ```
  > 1. Dans un autre terminal, accédez à la console shell du conteneur en cours d'exécution :
  >     ```shell
  >     kubectl exec -it redis -- /bin/bash
  >     ```
  > 1. Dans votre shell, allez dans `/data/redis`, puis créez un fichier :
  > 1. Dans votre shell, allez dans `/data/redis`, puis créez un fichier :
  >     ```shell
  >     root@redis:/data# cd /data/redis/
  >     root@redis:/data/redis# echo Hello > test-file
  >     ```
  > 1. Dans votre shell, listez les processus en cours d'exécution :
  >     ```shell
  >     root@redis:/data/redis# apt-get update
  >     root@redis:/data/redis# apt-get install procps
  >     root@redis:/data/redis# ps aux
  >     ```
  >     La sortie ressemble à ceci :
  >     ```console
  >     USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
  >     redis        1  0.1  0.1  33308  3828 ?        Ssl  00:46   0:00 redis-server *:6379
  >     root        12  0.0  0.0  20228  3020 ?        Ss   00:47   0:00 /bin/bash
  >     root        15  0.0  0.0  17500  2072 ?        R+   00:48   0:00 ps aux
  >     ```
  > 1. Dans votre shell, arrêtez le processus Redis :
  >     ```shell
  >     root@redis:/data/redis# kill <pid>
  >     ```
  >     où `<pid>` est l'ID de processus Redis (PID).
  > 1. Dans votre terminal initial, surveillez les changements apportés au Pod de Redis. Éventuellement,
  > vous verrez quelque chose comme ça :
  > 1. Dans votre terminal initial, surveillez les changements apportés au Pod de Redis. Éventuellement,
  > vous verrez quelque chose comme ça :
  >     ```console
  >     NAME      READY     STATUS     RESTARTS   AGE
  >     redis     1/1       Running    0          13s
  >     redis     0/1       Completed  0         6m
  >     redis     1/1       Running    1         6m
  >     ```
  > A ce stade, le conteneur est terminé et redémarré. C'est dû au fait que le Pod de Redis a une
  > restartPolicy
  > fixé à `Always`.
  > 1. Accédez à la console shell du conteneur redémarré :
  >     ```shell
  >     kubectl exec -it redis -- /bin/bash
  >     ```
  > 1. Dans votre shell, allez dans `/data/redis`, et vérifiez que `test-file` est toujours là.
  >     ```shell
  >     root@redis:/data/redis# cd /data/redis/
  >     root@redis:/data/redis# ls
  >     test-file
  >     ```
  > 1. Supprimez le pod que vous avez créé pour cet exercice :
  >     ```shell
  >     kubectl delete pod redis
  >     ```
  > ##
  > * Voir Volume.
  > * Voir Pod.
  > * Voir Pod.
  > * En plus du stockage sur disque local fourni par `emptyDir`, Kubernetes supporte de nombreuses solutions de stockage connectées au réseau, y compris PD sur GCE et EBS sur EC2, qui sont préférés pour les données critiques et qui s'occuperont des autres détails tels que le montage et le démontage sur les nœuds. Voir Volumes pour plus de détails.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-memory-limit-exceeded`

**Question** (fr, troubleshooting): Que se passe-t-il si un conteneur dépasse sa limite de mémoire ?

**Reference answer:** Il peut être arrêté (OOMKilled), puis redémarré selon la politique de redémarrage.

**Relevant documentation:**
- `tasks/configure-pod-container/assign-memory-resource.md`, section: *Allouer des ressources mémoire aux conteneurs et aux pods > Dépasser la limite de mémoire d'un conteneur*
  > [Allouer des ressources mémoire aux conteneurs et aux pods > Dépasser la limite de mémoire d'un conteneur]
  > Un conteneur peut dépasser sa demande de mémoire si le nœud dispose de la mémoire disponible. Cependant, un conteneur n'est pas autorisé à utiliser plus que sa limite de mémoire. Si un conteneur alloue plus de mémoire que sa limite, le Conteneur devient un candidat à la terminaison. Si le conteneur continue à consommer de la mémoire au-delà de sa limite, le conteneur est arrêté.
  > Si un conteneur terminé peut être redémarré, le kubelet le redémarre, comme pour tout autre type d'échec d'exécution.
  > Dans cet exercice, vous créez un Pod qui tente d'allouer plus de mémoire que sa limite.
  > Voici le fichier de configuration d'un Pod qui contient un conteneur avec une demande de mémoire de 50 MiB et une limite de mémoire de 100 MiB :
  > Example file `pods/resource/memory-request-limit-2.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: memory-demo-2
  >   namespace: mem-example
  > spec:
  >   containers:
  >   - name: memory-demo-2-ctr
  >     image: polinux/stress
  >     resources:
  >       requests:
  >         memory: "50Mi"
  >       limits:
  >         memory: "100Mi"
  >     command: ["stress"]
  >     args: ["--vm", "1", "--vm-bytes", "250M", "--vm-hang", "1"]
  > ```
  > Dans la section `args` du fichier de configuration, vous pouvez voir que le conteneur
  > tentera d'allouer 250 MiB de mémoire, ce qui est bien au-dessus de la limite de 100 MiB.
  > Créez le Pod :
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/resource/memory-request-limit-2.yaml --namespace=mem-example
  > ```
  > Consultez des informations détaillées sur le Pod :
  > ```shell
  > kubectl get pod memory-demo-2 --namespace=mem-example
  > ```
  > A ce niveau, le conteneur est soit en train de tourner, soit stoppé. Répétez la commande précédente jusqu'à ce que le conteneur soit terminé :
  > ```shell
  > NAME            READY     STATUS      RESTARTS   AGE
  > memory-demo-2   0/1       OOMKilled   1          24s
  > ```
  > Obtenez une vue plus détaillée de l'état du conteneur :
  > ```shell
  > kubectl get pod memory-demo-2 --output=yaml --namespace=mem-example
  > ```
  > La sortie indique que le conteneur a été stoppé suite à un manque de mémoire (OOM) :
  > ```shell
  > lastState:
  >    terminated:
  >      containerID: docker://65183c1877aaec2e8427bc95609cc52677a454b56fcb24340dbd22917c23b10f
  >      exitCode: 137
  >      finishedAt: 2017-06-20T20:52:19Z
  >      reason: OOMKilled
  >      startedAt: null
  > ```
  > Le conteneur dans cet exercice pourra être redémarré, ainsi le kubelet le redémarre. Répéter
  > cette commande plusieurs fois pour s'assurer que le conteneur est stoppé et redémarré d'une manière répététive :
  > ```shell
  > kubectl get pod memory-demo-2 --namespace=mem-example
  > ```
  > La sortie permet de voir que le conteneur est stoppé, redémarré, stoppé à nouveau, redémarré, et ainsi de suite :
  > ```
  > kubectl get pod memory-demo-2 --namespace=mem-example
  > NAME            READY     STATUS      RESTARTS   AGE
  > memory-demo-2   0/1       OOMKilled   1          37s
  > ```
  > ```
  > kubectl get pod memory-demo-2 --namespace=mem-example
  > NAME            READY     STATUS    RESTARTS   AGE
  > memory-demo-2   1/1       Running   2          40s
  > ```
  > Affichez des informations détaillées sur l'historique du Pod :
  > ```
  > kubectl describe pod memory-demo-2 --namespace=mem-example
  > ```
  > La sortie indique que le conteneur se démarre et échoue continuellement :
  > ```
  > ... Normal  Created   Created container with id 66a3a20aa7980e61be4922780bf9d24d1a1d8b7395c09861225b0eba1b1f8511
  > ... Warning BackOff   Back-off restarting failed container
  > ```
  > Affichez des informations détaillées sur les nœuds de votre cluster :
  > Affichez des informations détaillées sur les nœuds de votre cluster :
  > ```
  > kubectl describe nodes
  > ```
  > La sortie inclut un enregistrement de la mise à mort du conteneur suite à une condition hors mémoire :
  > ```
  > Warning OOMKilling Memory cgroup out of memory: Kill process 4481 (stress) score 1994 or sacrifice child
  > ```
  > Supprimez votre Pod :
  > ```shell
  > kubectl delete pod memory-demo-2 --namespace=mem-example
  > ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-env-var`

**Question** (fr, task): Comment définir une variable d'environnement pour un conteneur ?

**Reference answer:** Ajouter un champ `env` avec `name` et `value` dans la spécification du conteneur.

**Relevant documentation:**
- `tasks/inject-data-application/define-environment-variable-container.md`, section: *Définir des variables d'environnement pour un Container > Définir une variable d'environnement pour un container*
  > [Définir des variables d'environnement pour un Container > Définir une variable d'environnement pour un container]
  > Lorsque vous créez un Pod, vous pouvez définir des variables d'environnement
  > pour les containers qui seront exécutés au sein du Pod.
  > Pour les définir, utilisez le champ `env` ou `envFrom`
  > dans le fichier de configuration.
  > Dans cet exercice, vous allez créer un Pod qui exécute un container. Le fichier de configuration pour ce Pod contient une variable d'environnement s'appelant `DEMO_GREETING` et sa valeur est `"Hello from the environment"`. Voici le fichier de configuration du Pod:
  > Example file `pods/inject/envars.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: envar-demo
  >   labels:
  >     purpose: demonstrate-envars
  > spec:
  >   containers:
  >   - name: envar-demo-container
  >     image: gcr.io/google-samples/node-hello:1.0
  >     env:
  >     - name: DEMO_GREETING
  >       value: "Hello from the environment"
  >     - name: DEMO_FAREWELL
  >       value: "Such a sweet sorrow"
  > ```
  > 1. Créez un Pod à partir de ce fichier:
  >    ```shell
  >    kubectl apply -f https://k8s.io/examples/pods/inject/envars.yaml
  >    ```
  > 1. Listez les Pods:
  >    ```shell
  >    kubectl get pods -l purpose=demonstrate-envars
  >    ```
  >    Le résultat sera similaire à celui-ci:
  >    Le résultat sera similaire à celui-ci:
  >    ```
  >    NAME            READY     STATUS    RESTARTS   AGE
  >    envar-demo      1/1       Running   0          9s
  >    ```
  > 1. Listez les variables d'environnement au sein du container:
  >    ```shell
  >    kubectl exec envar-demo -- printenv
  >    ```
  >    Le résultat sera similaire à celui-ci:
  >    ```
  >    NODE_VERSION=4.4.2
  >    EXAMPLE_SERVICE_PORT_8080_TCP_ADDR=10.3.245.237
  >    HOSTNAME=envar-demo
  >    ...
  >    DEMO_GREETING=Hello from the environment
  >    DEMO_FAREWELL=Such a sweet sorrow
  >    ```
  > Les variables d'environnement définies dans les champs `env` ou `envFrom`
  > écraseront les variables définies dans l'image utilisée par le container.
  > Une variable d'environnement peut faire référence à une autre variable,
  > cependant l'ordre de déclaration est important. Une variable faisant référence
  > à une autre doit être déclarée après la variable référencée.
  > De plus, il est recommandé d'éviter les références circulaires.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-secret-env`

**Question** (fr, task): Comment utiliser la valeur d'un Secret comme variable d'environnement ?

**Reference answer:** Dans `env`, utiliser `valueFrom.secretKeyRef` avec le nom du Secret et la clé.

**Relevant documentation:**
- `tasks/inject-data-application/distribute-credentials-secure.md`, section: *Distribuer des données sensibles de manière sécurisée avec les Secrets > Définir des variables d'environnement avec des Secrets*
  > [Distribuer des données sensibles de manière sécurisée avec les Secrets > Définir des variables d'environnement avec des Secrets]
  > Il est possible de monter les données des Secrets comme variables d'environnement dans vos containers.
  > Si un container consomme déja un Secret en variables d'environnement,
  > la mise à jour de ce Secret ne sera pas répercutée dans le container tant
  > qu'il n'aura pas été redémarré. Il existe cependant des solutions tierces
  > permettant de redémarrer les containers lors d'une mise à jour du Secret.
  > [Distribuer des données sensibles de manière sécurisée avec les Secrets > Définir des variables d'environnement avec des Secrets > Définir une variable d'environnement à partir d'un seul Secret]
  > *  Définissez une variable d'environnement et sa valeur à l'intérieur d'un Secret:
  >    ```shell
  >    kubectl create secret generic backend-user --from-literal=backend-username='backend-admin'
  >    ```
  > *  Assignez la valeur de `backend-username` définie dans le Secret
  >    à la variable d'environnement `SECRET_USERNAME` dans la configuration du Pod.
  > Example file `pods/inject/pod-single-secret-env-variable.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: env-single-secret
  > spec:
  >   containers:
  >   - name: envars-test-container
  >     image: nginx
  >     env:
  >     - name: SECRET_USERNAME
  >       valueFrom:
  >         secretKeyRef:
  >           name: backend-user
  >           key: backend-username
  > ```
  > *  Créez le Pod:
  >    ```shell
  >    kubectl create -f https://k8s.io/examples/pods/inject/pod-single-secret-env-variable.yaml
  >    ```
  > *  À l'intérieur d'une session shell, affichez le contenu de la variable
  >    d'environnement `SECRET_USERNAME`:
  >    ```shell
  >    kubectl exec -i -t env-single-secret -- /bin/sh -c 'echo $SECRET_USERNAME'
  >    ```
  >    Le résultat est:
  >    ```
  >    backend-admin
  >    ```
  > [Distribuer des données sensibles de manière sécurisée avec les Secrets > Définir des variables d'environnement avec des Secrets > Définir des variables d'environnement à partir de plusieurs Secrets]
  > *  Comme précédemment, créez d'abord les Secrets:
  >    ```shell
  >    kubectl create secret generic backend-user --from-literal=backend-username='backend-admin'
  >    kubectl create secret generic db-user --from-literal=db-username='db-admin'
  >    ```
  > *  Définissez les variables d'environnement dans la configuration du Pod.
  > Example file `pods/inject/pod-multiple-secret-env-variable.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: envvars-multiple-secrets
  > spec:
  >   containers:
  >   - name: envars-test-container
  >     image: nginx
  >     env:
  >     - name: BACKEND_USERNAME
  >       valueFrom:
  >         secretKeyRef:
  >           name: backend-user
  >           key: backend-username
  >     - name: DB_USERNAME
  >       valueFrom:
  >         secretKeyRef:
  >           name: db-user
  >           key: db-username
  > ```
  > *  Créez le Pod:
  >    ```shell
  >    kubectl create -f https://k8s.io/examples/pods/inject/pod-multiple-secret-env-variable.yaml
  >    ```
  > *  Dans un shell, listez les variables d'environnement du container:
  >    ```shell
  >    kubectl exec -i -t envvars-multiple-secrets -- /bin/sh -c 'env | grep _USERNAME'
  >    ```
  >    Le résultat est:
  >    ```
  >    DB_USERNAME=db-admin
  >    BACKEND_USERNAME=backend-admin
  >    ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-exec-shell`

**Question** (fr, command): Comment ouvrir un shell dans un conteneur en cours d'exécution ?

**Reference answer:** `kubectl exec -it <pod> -- /bin/bash`.

**Relevant documentation:**
- `tasks/debug-application-cluster/get-shell-running-container.md`, section: *Obtenez un shell dans un conteneur en cours d'exécution > Obtenir un shell dans un conteneur*
  > [Obtenez un shell dans un conteneur en cours d'exécution > Obtenir un shell dans un conteneur]
  > Dans cet exercice, vous allez créer un pod contenant un conteneur.
  > Le conteneur exécute une image nginx.
  > Voici le fichier de configuration du Pod:
  > Example file `application/shell-demo.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: shell-demo
  > spec:
  >   volumes:
  >   - name: shared-data
  >     emptyDir: {}
  >   containers:
  >   - name: nginx
  >     image: nginx
  >     volumeMounts:
  >     - name: shared-data
  >       mountPath: /usr/share/nginx/html
  >   hostNetwork: true
  >   dnsPolicy: Default
  > ```
  > Créez le Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/application/shell-demo.yaml
  > ```
  > Vérifiez que le conteneur est en cours d'exécution:
  > ```shell
  > kubectl get pod shell-demo
  > ```
  > Obtenez un shell pour le conteneur en cours d'exécution:
  > ```shell
  > kubectl exec -it shell-demo -- /bin/bash
  > ```
  > Le double tiret "-" est utilisé pour séparer les arguments que vous souhaitez passer à la commande des arguments kubectl.
  > Dans votre shell, listez le répertoire racine:
  > ```shell
  > root@shell-demo:/# ls /
  > ```
  > Dans votre shell, testez d'autres commandes.
  > Voici quelques exemples:
  > Dans votre shell, testez d'autres commandes.
  > Voici quelques exemples:
  > ```shell
  > root@shell-demo:/# ls /
  > root@shell-demo:/# cat /proc/mounts
  > root@shell-demo:/# cat /proc/1/maps
  > root@shell-demo:/# apt-get update
  > root@shell-demo:/# apt-get install -y tcpdump
  > root@shell-demo:/# tcpdump
  > root@shell-demo:/# apt-get install -y lsof
  > root@shell-demo:/# lsof
  > root@shell-demo:/# apt-get install -y procps
  > root@shell-demo:/# ps aux
  > root@shell-demo:/# ps aux | grep nginx
  > ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-port-forward`

**Question** (fr, command): Comment accéder depuis ma machine au port d'un Pod sans l'exposer ?

**Reference answer:** `kubectl port-forward` vers le Pod, par ex. `kubectl port-forward pods/<nom> 28015:27017`.

**Relevant documentation:**
- `tasks/access-application-cluster/port-forward-access-application-cluster.md`, section: *Utiliser le Port Forwarding pour accéder à des applications dans un cluster > Rediriger un port local vers un port du pod*
  > [Utiliser le Port Forwarding pour accéder à des applications dans un cluster > Rediriger un port local vers un port du pod]
  > 1. `kubectl port-forward` permet d'utiliser un nom de ressource, tel qu'un nom de pod, pour sélectionner un pod correspondant vers lequel rediriger le port.
  >    ```shell
  >    # Changez mongo-75f59d57f4-4nd6q par le nom du pod
  >    kubectl port-forward mongo-75f59d57f4-4nd6q 28015:27017
  >    ```
  >    qui est identique à
  >    ```shell
  >    kubectl port-forward pods/mongo-75f59d57f4-4nd6q 28015:27017
  >    ```
  >    ou
  >    ```shell
  >    kubectl port-forward deployment/mongo 28015:27017
  >    ```
  >    ou
  >    ```shell
  >    kubectl port-forward replicaset/mongo-75f59d57f4 28015:27017
  >    ```
  >    ou
  >    ```shell
  >    kubectl port-forward service/mongo 28015:27017
  >    ```
  >    N'importe laquelle des commandes ci-dessus fonctionne. Le résultat sera similaire à ceci :
  >    ```
  >    Forwarding from 127.0.0.1:28015 -> 27017
  >    Forwarding from [::1]:28015 -> 27017
  >    ```
  >    `kubectl port-forward` ne se termine pas une fois le port-forward lancé. Pour continuer avec les exercices, vous devrez ouvrir un autre terminal.
  > 2. Démarrez l'interface de ligne de commande MongoDB :
  >    ```shell
  >    mongosh --port 28015
  >    ```
  > 3. Depuis la ligne de commande de MongoDB, entrez la commande `ping` :
  > 3. Depuis la ligne de commande de MongoDB, entrez la commande `ping` :
  >    ```
  >    db.runCommand( { ping: 1 } )
  >    ```
  >    Une demande de ping réussie renvoie :
  >    ```
  >    { ok: 1 }
  >    ```
  > [Utiliser le Port Forwarding pour accéder à des applications dans un cluster > Rediriger un port local vers un port du pod > Laisser _kubectl_ choisir le port local {#let-kubectl-choose-local-port}]
  > Si vous n'avez pas besoin d'un port local précis,
  > vous pouvez laisser `kubectl` choisir et attribuer le port local,
  > vous évitant ainsi de gérer les conflits de ports locaux, avec cette syntaxe légèrement plus simple :
  > ```shell
  > kubectl port-forward deployment/mongo :27017
  > ```
  > `kubectl` trouvera un numéro de port local qui n'est pas utilisé
  > (en évitant les numéros de ports bas, car ils pourraient être utilisés par d'autres applications).
  > Le résultat sera similaire à :
  > ```
  > Forwarding from 127.0.0.1:63753 -> 27017
  > Forwarding from [::1]:63753 -> 27017
  > ```

*Drafting note:* golden v2 draft (2026-11-07) | self-check: aligned with the referenced text

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-qos`

**Question** (fr, concept): Quelles sont les classes de qualité de service (QoS) d'un Pod ?

**Reference answer:** Guaranteed, Burstable et BestEffort, attribuées selon les requests et limits de CPU et de mémoire des conteneurs.

**Relevant documentation:**
- `tasks/configure-pod-container/quality-service-pod.md`, section: *(whole document)*
  > [Configurer la qualité de service pour les pods]
  > Cette page montre comment configurer les Pods pour qu'ils soient affectés à des classes particulières de qualité de service (QoS). Kubernetes utilise des classes de QoS pour prendre des décisions concernant l'ordonnancement et les évictions des pods.
  > ##
  > [Configurer la qualité de service pour les pods > Les Classes de QoS]
  > Quand Kubernetes crée un Pod, il affecte une de ces classes QoS au Pod :
  > * Guaranteed
  > * Burstable
  > * BestEffort
  > [Configurer la qualité de service pour les pods > Créez un namespace]
  > Créez un namespace de manière à ce que les ressources que vous créez dans cet exercice soient isolées du reste de votre cluster.
  > ```shell
  > kubectl create namespace qos-example
  > ```
  > [Configurer la qualité de service pour les pods > Créez un Pod qui se fait attribuer une classe QoS de Guaranteed]
  > Pour qu'un Pod reçoive une classe de QoS Guaranteed :
  > * Chaque conteneur du Pod doit avoir une limite de mémoire et une demande de mémoire, et elles doivent être les mêmes.
  > * Chaque conteneur dans le Pod doit avoir une limite CPU et une demande CPU, et ils doivent être les mêmes.
  > Ci-dessous le fichier de configuration d'un Pod qui a un seul conteneur.
  > Le conteneur dispose d'une limite de mémoire et d'une demande de mémoire, tous deux égaux à 200 MiB. Le conteneur a également une limite CPU et une demande CPU, toutes deux égales à 700 milliCPU :
  > Example file `pods/qos/qos-pod.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: qos-demo
  >   namespace: qos-example
  > spec:
  >   containers:
  >   - name: qos-demo-ctr
  >     image: nginx
  >     resources:
  >       limits:
  >         memory: "200Mi"
  >         cpu: "700m"
  >       requests:
  >         memory: "200Mi"
  >         cpu: "700m"
  > ```
  > Créez le Pod :
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/qos/qos-pod.yaml --namespace=qos-example
  > ```
  > Consultez des informations détaillées sur le Pod :
  > ```shell
  > kubectl get pod qos-demo --namespace=qos-example --output=yaml
  > ```
  > ```shell
  > kubectl get pod qos-demo --namespace=qos-example --output=yaml
  > ```
  > Le résultat indique que Kubernetes a donné au pod une classe de qualité de service de type Guaranteed. De plus, il affiche que la demande de mémoire du conteneur du pod correspond à sa limite de mémoire, et que la demande de CPU correspond à sa limite de CPU.
  > ```yaml
  > spec:
  >   containers:
  >     ...
  >     resources:
  >       limits:
  >         cpu: 700m
  >         memory: 200Mi
  >       requests:
  >         cpu: 700m
  >         memory: 200Mi
  >   ...
  > status:
  >   qosClass: Guaranteed
  > ```
  > Si un conteneur spécifie sa propre limite de mémoire, mais ne spécifie pas de demande de mémoire, Kubernetes attribue automatiquement une demande de mémoire correspondant à la limite. De même, si un conteneur spécifie sa propre limite CPU, mais ne spécifie pas de demande de CPU, Kubernetes lui attribue automatiquement une demande de CPU qui correspond à cette limite.
  > Supprimez votre Pod :
  > ```shell
  > kubectl delete pod qos-demo --namespace=qos-example
  > ```
  > [Configurer la qualité de service pour les pods > Créez un Pod qui se fait attribuer une classe QoS de type Burstable]
  > Un Pod reçoit une classe QoS de Burstable si :
  > * Le Pod ne répond pas aux critères de la classe QoS Guaranteed.
  > * Au moins un conteneur dans le Pod dispose d'une demande de mémoire ou de CPU.
  > Voici le fichier de configuration d'un pod qui a un seul conteneur. Le conteneur a une limite de mémoire de 200 MiB et une demande de mémoire de 100 MiB.
  > Example file `pods/qos/qos-pod-2.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: qos-demo-2
  >   namespace: qos-example
  > spec:
  >   containers:
  >   - name: qos-demo-2-ctr
  >     image: nginx
  >     resources:
  >       limits:
  >         memory: "200Mi"
  >       requests:
  >         memory: "100Mi"
  > ```
  > Créez le Pod :
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/qos/qos-pod-2.yaml --namespace=qos-example
  > ```
  > Consultez des informations détaillées sur le Pod :
  > ```shell
  > kubectl get pod qos-demo-2 --namespace=qos-example --output=yaml
  > ```
  > La sortie montre que Kubernetes a accordé au pod une classe QoS de type Burstable.
  > ```yaml
  > spec:
  >   containers:
  >   - image: nginx
  >     imagePullPolicy: Always
  >     name: qos-demo-2-ctr
  >     resources:
  >       limits:
  >         memory: 200Mi
  >       requests:
  >         memory: 100Mi
  >   ...
  > status:
  >   qosClass: Burstable
  > ```
  > Supprimez votre Pod :
  > ```shell
  > kubectl delete pod qos-demo-2 --namespace=qos-example
  > ```
  > [Configurer la qualité de service pour les pods > Créez un Pod qui se fait attribuer une classe QoS de type BestEffort]
  > Pour qu'un pod puisse avoir la classe QoS de BestEffort, les conteneurs dans le pod ne doivent pas
  > avoir des limites ou des demandes de mémoire ou de CPU.
  > Voici le fichier de configuration d'un Pod qui a un seul conteneur. Le conteneur n'a pas des limites ou des demandes de mémoire ou de CPU :
  > Example file `pods/qos/qos-pod-3.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: qos-demo-3
  >   namespace: qos-example
  > spec:
  >   containers:
  >   - name: qos-demo-3-ctr
  >     image: nginx
  > ```
  > Créez le Pod :
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/qos/qos-pod-3.yaml --namespace=qos-example
  > ```
  > Consultez des informations détaillées sur le Pod :
  > ```shell
  > kubectl get pod qos-demo-3 --namespace=qos-example --output=yaml
  > ```
  > Le résultat montre que Kubernetes a accordé au pod une classe QoS de BestEffort.
  > ```yaml
  > spec:
  >   containers:
  >     ...
  >     resources: {}
  >   ...
  > status:
  >   qosClass: BestEffort
  > ```
  > Supprimez votre Pod :
  > ```shell
  > kubectl delete pod qos-demo-3 --namespace=qos-example
  > ```
  > [Configurer la qualité de service pour les pods > Créez un pod qui contient deux conteneurs]
  > Voici le fichier de configuration d'un Pod qui a deux conteneurs. Un conteneur spécifie une
  > demande de mémoire de 200 MiB. L'autre conteneur ne spécifie aucune demande ou limite.
  > Example file `pods/qos/qos-pod-4.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: qos-demo-4
  >   namespace: qos-example
  > spec:
  >   containers:
  >   - name: qos-demo-4-ctr-1
  >     image: nginx
  >     resources:
  >       … (section continues)

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-node-label`

**Question** (fr, task): Comment forcer un Pod à tourner sur un nœud qui porte un label précis ?

**Reference answer:** Ajouter un label au nœud (`kubectl label nodes <nœud> disktype=ssd`), puis un `nodeSelector` correspondant dans le Pod.

**Relevant documentation:**
- `tasks/configure-pod-container/assign-pods-nodes.md`, section: *Assigner des pods aux nœuds > Ajouter un label à un nœud*
  > [Assigner des pods aux nœuds > Ajouter un label à un nœud]
  > 1. Listez les nœuds de votre cluster :
  >     ```shell
  >     kubectl get nodes
  >     ```
  >     La sortie est la suivante :
  >     ```shell
  >     NAME      STATUS    ROLES     AGE     VERSION
  >     worker0   Ready     <none>    1d      v1.13.0
  >     worker1   Ready     <none>    1d      v1.13.0
  >     worker2   Ready     <none>    1d      v1.13.0
  >     ```
  > 2. Choisissez l'un de vos nœuds et ajoutez-y un label :
  >     ```shell
  >     kubectl label nodes <your-node-name> disktype=ssd
  >     ```
  >     où `<your-node-name>` est le nom du noeud que vous avez choisi.
  > 3. Vérifiez que le nœud que vous avez choisi a le label `disktype=ssd` :
  >     ```shell
  >     kubectl get nodes --show-labels
  >     ```
  >     La sortie est la suivante :
  >     ```shell
  >     NAME      STATUS    ROLES    AGE     VERSION        LABELS
  >     worker0   Ready     <none>   1d      v1.13.0        ...,disktype=ssd,kubernetes.io/hostname=worker0
  >     worker1   Ready     <none>   1d      v1.13.0        ...,kubernetes.io/hostname=worker1
  >     worker2   Ready     <none>   1d      v1.13.0        ...,kubernetes.io/hostname=worker2
  >     ```
  >     Dans la sortie précédente, vous constatez que le nœud `worker0` possède le label `disktype=ssd`.
- `tasks/configure-pod-container/assign-pods-nodes.md`, section: *Assigner des pods aux nœuds > Créez un pod qui sera planifié sur un nœud sélectionné.*
  > [Assigner des pods aux nœuds > Créez un pod qui sera planifié sur un nœud sélectionné.]
  > Le fichier de configuration de pod décrit un pod qui possède un selector de nœud de type `disktype:ssd`. Cela signifie que le pod sera planifié sur un nœud ayant le label `disktype=ssd`.
  > Example file `pods/pod-nginx.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: nginx
  >   labels:
  >     env: test
  > spec:
  >   containers:
  >   - name: nginx
  >     image: nginx
  >     imagePullPolicy: IfNotPresent
  >   nodeSelector:
  >     disktype: ssd
  > ```
  > 1. Utilisez le fichier de configuration pour créer un pod qui sera ordonnancé sur votre nœud choisi :
  >     ```shell
  >     kubectl apply -f https://k8s.io/examples/pods/pod-nginx.yaml
  >     ```
  > 2. Vérifiez que le pod fonctionne sur le nœud que vous avez choisi :
  >     ```shell
  >     kubectl get pods --output=wide
  >     ```
  >     La sortie est la suivante :
  >     ```shell
  >     NAME     READY     STATUS    RESTARTS   AGE    IP           NODE
  >     nginx    1/1       Running   0          13s    10.200.0.4   worker0
  >     ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-hpa`

**Question** (fr, task): Comment créer un autoscaler horizontal pour un déploiement ?

**Reference answer:** `kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10`.

**Relevant documentation:**
- `tasks/run-application/horizontal-pod-autoscale-walkthrough.md`, section: *Découverte de l'HorizontalPodAutoscaler > Créer le HorizontalPodAutoscaler*
  > [Découverte de l'HorizontalPodAutoscaler > Créer le HorizontalPodAutoscaler {#create-horizontal-pod-autoscaler}]
  > Maintenant que le serveur est en cours d'exécution, créez l'autoscaler à l'aide de `kubectl`.
  > Il existe une sous-commande `kubectl autoscale`,
  > faisant partie de `kubectl`, qui vous aide à le faire.
  > Vous allez bientôt exécuter une commande qui crée un HorizontalPodAutoscaler
  > qui maintient entre 1 et 10 réplicas des Pods contrôlés par le déploiement
  > php-apache que vous avez créé lors de la première étape.
  > En parlant simplement, le HPA (contrôleur)
  > augmentera ou diminuera le nombre de réplicas (en mettant à jour le déploiement)
  > pour maintenir une utilisation CPU moyenne de 50% sur l'ensemble des Pods.
  > Ensuite, le déploiement met à jour le ReplicaSet - cela fait partie du
  > fonctionnement de tous les déploiements dans Kubernetes - puis le ReplicaSet
  > ajoute ou supprime des Pods en fonction des modifications apportées à son champ `.spec`.
  > Étant donné que chaque pod demande 200 milli-cores via `kubectl run`,
  > cela signifie une utilisation CPU moyenne de 100 milli-cores.
  > Consultez les détails de l'algorithme pour plus d'informations sur celui-ci.
  > Créez le HorizontalPodAutoscaler :
  > ```shell
  > kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
  > ```
  > ```shell
  > kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
  > ```
  > ```
  > horizontalpodautoscaler.autoscaling/php-apache autoscaled
  > ```
  > Vous pouvez visualiser le statut actuel du nouvel HorizontalPodAutoscaler avec la commande:
  > ```shell
  > # Vous pouvez utiliser "hpa" ou "horizontalpodautoscaler"; les deux appelations fonctionnent.
  > kubectl get hpa
  > ```
  > Le résultat sera similaire à celui-ci:
  > ```
  > NAME         REFERENCE                     TARGET    MINPODS   MAXPODS   REPLICAS   AGE
  > php-apache   Deployment/php-apache/scale   0% / 50%  1         10        1          18s
  > ```
  > (Si vous voyez d'autres HorizontalPodAutoscalers avec des noms différents,
  > cela signifie qu'ils existaient déjà et ce n'est généralement pas un problème).
  > Veuillez noter que la consommation actuelle de CPU est de 0 %
  > car il n'y a pas de clients envoyant des requêtes au serveur
  > (la colonne ``TARGET`` montre la moyenne de tous les Pods
  > contrôlés par le déploiement correspondant).

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-node-status`

**Question** (fr, troubleshooting): Comment voir l'état et les conditions d'un nœud ?

**Reference answer:** `kubectl describe node <nom>` ; l'état comprend notamment les conditions (Ready, MemoryPressure, DiskPressure…).

**Relevant documentation:**
- `concepts/architecture/nodes.md`, section: *Noeuds > État du nœud*
  > [Noeuds > État du nœud]
  > L'état d'un Nœud contient les informations suivantes :
  > * Adresses
  > * Conditions
  > * Capacité et Allocatable
  > * Info
  > Vous pouvez utiliser `kubectl` pour afficher l'état d'un Nœud et d'autres détails :
  > ```shell
  > kubectl describe node <insérez-le-nom-du-nœud-ici>
  > ```
  > Consultez État du nœud pour plus de détails.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-netpol-limit-service`

**Question** (fr, task): Comment limiter l'accès à un Service aux seuls Pods qui portent un label précis ?

**Reference answer:** Créer une NetworkPolicy qui sélectionne les Pods du Service et n'autorise l'ingress que depuis les Pods portant le label voulu (par ex. `access: "true"`).

**Relevant documentation:**
- `tasks/administer-cluster/declare-network-policy.md`, section: *Déclarer une politique réseau (NetworkPolicy) > Limiter l'accès au Service `nginx`*
  > [Déclarer une politique réseau (NetworkPolicy) > Limiter l'accès au Service `nginx`]
  > Pour limiter l'accès au service `nginx` afin que seuls les pods avec le label `access: true` puissent le consulter, créez un objet NetworkPolicy comme suit :
  > Example file `service/networking/nginx-policy.yaml`:
  > ```yaml
  > apiVersion: networking.k8s.io/v1
  > kind: NetworkPolicy
  > metadata:
  >   name: access-nginx
  > spec:
  >   podSelector:
  >     matchLabels:
  >       app: nginx
  >   ingress:
  >   - from:
  >     - podSelector:
  >         matchLabels:
  >           access: "true"
  > ```
  > Le nom d'un objet NetworkPolicy doit être un nom de sous-domaine DNS valide.
  > Les NetworkPolicy incluent un `podSelector` qui sélectionne le regroupement de pods auxquels la politique s'applique. Vous pouvez voir que cette politique sélectionne les pods avec le label `app=nginx`. Ce label a été ajouté automatiquement au pod dans le déploiement `nginx`. Un `podSelector` vide sélectionne tous les pods dans le namespace.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---
