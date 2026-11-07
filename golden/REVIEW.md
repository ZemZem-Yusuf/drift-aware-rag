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

### `node-selector-ssd`

**Question** (en, task): How do I make a pod run only on nodes that have an SSD?

**Reference answer:** Attach a label to the nodes that have an SSD (labels can be attached manually, e.g. `disktype=ssd`) and add a matching `nodeSelector`, or a node affinity rule of type `requiredDuringSchedulingIgnoredDuringExecution`, to the Pod spec. A `preferredDuringSchedulingIgnoredDuringExecution` rule is only a preference: if no matching node is available, the Pod is still scheduled.

**Relevant documentation:**
- `concepts/scheduling-eviction/assign-pod-node.md`, section: *Assigning Pods to Nodes > Node labels*
  > [Assigning Pods to Nodes > Node labels {#built-in-node-labels}]
  > Like many other Kubernetes objects, nodes have
  > labels. You can
  > attach labels manually.
  > Kubernetes also populates a standard set of labels
  > on all nodes in a cluster.
  > The value of these labels is cloud provider specific and is not guaranteed to be reliable.
  > For example, the value of `kubernetes.io/hostname` may be the same as the node name in some environments
  > and a different value in other environments.
  > [Assigning Pods to Nodes > Node labels {#built-in-node-labels} > Node isolation/restriction]
  > Adding labels to nodes allows you to target Pods for scheduling on specific
  > nodes or groups of nodes. You can use this functionality to ensure that specific
  > Pods only run on nodes with certain isolation, security, or regulatory
  > properties.
  > If you use labels for node isolation, choose label keys that the kubelet
  > cannot modify. This prevents a compromised node from setting those labels on
  > itself so that the scheduler schedules workloads onto the compromised node.
  > The `NodeRestriction` admission plugin
  > prevents the kubelet from setting or modifying labels with a
  > `node-restriction.kubernetes.io/` prefix.
  > To make use of that label prefix for node isolation:
  > 1. Ensure you are using the Node authorizer and have _enabled_ the `NodeRestriction` admission plugin.
  > 2. Add labels with the `node-restriction.kubernetes.io/` prefix to your nodes, and use those labels in your node selectors.
  >    For example, `example.com.node-restriction.kubernetes.io/fips=true` or `example.com.node-restriction.kubernetes.io/pci-dss=true`.
- `concepts/scheduling-eviction/assign-pod-node.md`, section: *Assigning Pods to Nodes > nodeSelector*
  > [Assigning Pods to Nodes > nodeSelector]
  > `nodeSelector` is the simplest recommended form of node selection constraint.
  > You can add the `nodeSelector` field to your Pod specification and specify the
  > node labels you want the target node to have.
  > Kubernetes only schedules the Pod onto nodes that have each of the labels you
  > specify.
  > See Assign Pods to Nodes for more
  > information.
- `concepts/scheduling-eviction/assign-pod-node.md`, section: *Assigning Pods to Nodes > Affinity and anti-affinity*
  > [Assigning Pods to Nodes > Affinity and anti-affinity]
  > `nodeSelector` is the simplest way to constrain Pods to nodes with specific
  > labels. Affinity and anti-affinity expand the types of constraints you can
  > define. Some of the benefits of affinity and anti-affinity include:
  > - The affinity/anti-affinity language is more expressive. `nodeSelector` only
  >   selects nodes with all the specified labels. Affinity/anti-affinity gives you
  >   more control over the selection logic.
  > - You can indicate that a rule is *soft* or *preferred*, so that the scheduler
  >   still schedules the Pod even if it can't find a matching node.
  > - You can constrain a Pod using labels on other Pods running on the node (or other topological domain),
  >   instead of just node labels, which allows you to define rules for which Pods
  >   can be co-located on a node.
  > The affinity feature consists of two types of affinity:
  > - *Node affinity* functions like the `nodeSelector` field but is more expressive and
  >   allows you to specify soft rules.
  > - *Inter-pod affinity/anti-affinity* allows you to constrain Pods against labels
  >   on other Pods.
  > [Assigning Pods to Nodes > Affinity and anti-affinity > Node affinity]
  > Node affinity is conceptually similar to `nodeSelector`, allowing you to constrain which nodes your
  > Pod can be scheduled on based on node labels. There are two types of node
  > affinity:
  > - `requiredDuringSchedulingIgnoredDuringExecution`: The scheduler can't
  >   schedule the Pod unless the rule is met. This functions like `nodeSelector`,
  >   but with a more expressive syntax.
  > - `preferredDuringSchedulingIgnoredDuringExecution`: The scheduler tries to
  >   find a node that meets the rule. If a matching node is not available, the
  >   scheduler still schedules the Pod.
  > In the preceding types, `IgnoredDuringExecution` means that if the node labels
  > change after Kubernetes schedules the Pod, the Pod continues to run.
  > You can specify node affinities using the `.spec.affinity.nodeAffinity` field in
  > your Pod spec.
  > For example, consider the following Pod spec:
  > For example, consider the following Pod spec:
  > Example file `pods/pod-with-node-affinity.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: with-node-affinity
  > spec:
  >   affinity:
  >     nodeAffinity:
  >       requiredDuringSchedulingIgnoredDuringExecution:
  >         nodeSelectorTerms:
  >         - matchExpressions:
  >           - key: topology.kubernetes.io/zone
  >             operator: In
  >             values:
  >             - antarctica-east1
  >             - antarctica-west1
  >       preferredDuringSchedulingIgnoredDuringExecution:
  >       - weight: 1
  >         preference:
  >           matchExpressions:
  >           - key: another-node-label-key
  >             operator: In
  >             values:
  >             - another-node-label-value
  >   containers:
  >   - name: with-node-affinity
  >     image: registry.k8s.io/pause:3.8
  > ```
  > In this example, the following rules apply:
  > - The node *must* have a label with the key `topology.kubernetes.io/zone` and
  >   the value of that label *must* be either `antarctica-east1` or `antarctica-west1`.
  > - The node *preferably* has a label with the key `another-node-label-key` and
  >   the value `another-node-label-value`.
  > You can use the `operator` field to specify a logical operator for Kubernetes to use when
  > interpreting the rules. You can use `In`, `NotIn`, `Exists`, `DoesNotExist`,
  > `Gt` and `Lt`.
  > Read Operators
  > to learn more about how these work.
  > `NotIn` and `DoesNotExist` allow you to define node anti-affinity behavior.
  > Alternatively, you can use node taints
  > to repel Pods from specific nodes.
  > If you specify both `nodeSelector` and `nodeAffinity`, *both* must be satisfied
  > for the Pod to be scheduled onto a node.
  > If you specify multiple terms in `nodeSelectorTerms` associated with `nodeAffinity`
  > types, then the Pod can be scheduled onto a node if one of the specified terms
  > can be satisfied (terms are ORed).
  > If you specify multiple expressions in a single `matchExpressions` field associated with a
  > term in `nodeSelectorTerms`, then the Pod can be scheduled onto a node only
  > if all the expressions are satisfied (expressions are ANDed).
  > See Assign Pods to Nodes using Node Affinity
  > for more information.
  > [Assigning Pods to Nodes > Affinity and anti-affinity > Node affinity > Node affinity weight]
  > You can specify a `weight` between 1 and 100 for each instance of the
  > `preferredDuringSchedulingIgnoredDuringExecution` affinity type. When the
  > scheduler finds nodes that meet all the other scheduling requirements of the Pod, the
  > scheduler iterates through every preferred rule that the node satisfies and adds the
  > value of the `weight` for that expression to a sum.
  > The final sum is added to the score of other priority functions for the node.
  > Nodes with the highest total score are prioritized when the scheduler makes a
  > scheduling decision for the Pod.
  > For example, consider the following Pod spec:
  > For example, consider the following Pod spec:
  > Example file `pods/pod-with-affinity-preferred-weight.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: with-affinity-preferred-weight
  > spec:
  >   affinity:
  >     nodeAffinity:
  >       requiredDuringSchedulingIgnoredDuringExecution:
  >         nodeSelectorTerms:
  >         - matchExpressions:
  >           - key: kubernetes.io/os
  >             operator: In
  >             values:
  >             - linux
  >       preferredDuringSchedulingIgnoredDuringExecution:
  >       - weight: 1
  >         preference:
  >           matchExpressions:
  >           - key: label-1
  >             operator: In
  >             values:
  >             - key-1
  >       - weight: 50
  >         preference:
  >           matchExpressions:
  >           - key: label-2
  >             operator: In
  >             values:
  >             - key-2
  >   containers:
  >   - name: with-node-affinity
  >     image: registry.k8s.io/pause:3.8
  > ```
  > If there are two possible nodes that match the
  > `preferredDuringSchedulingIgnoredDuringExecution` rule, one with the
  > `label-1:key-1` label and another with the `label-2:key-2` label, the scheduler
  > considers the `weight` of each node and adds the weight to … (section continues)

*Drafting note:* human review (Youssef Zemzem, 2026-11-07): added the node-labels section; no kubectl command claimed | human review 2 (Youssef Zemzem, 2026-11-07): required vs preferred affinity made explicit

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `statefulset-vs-deployment`

**Question** (en, concept): When should I use a StatefulSet instead of a Deployment?

**Reference answer:** When the application needs stable, unique network identifiers, stable persistent storage, or ordered, graceful deployment and scaling.

**Relevant documentation:**
- `concepts/workloads/controllers/statefulset.md`, section: *StatefulSets > Using StatefulSets*
  > [StatefulSets > Using StatefulSets]
  > StatefulSets are valuable for applications that require one or more of the
  > following.
  > * Stable, unique network identifiers.
  > * Stable, persistent storage.
  > * Ordered, graceful deployment and scaling.
  > * Ordered, automated rolling updates.
  > In the above, stable is synonymous with persistence across Pod (re)scheduling.
  > If an application doesn't require any stable identifiers or ordered deployment,
  > deletion, or scaling, you should deploy your application using a workload object
  > that provides a set of stateless replicas.
  > Deployment or
  > ReplicaSet may be better suited to your stateless needs.
- `concepts/workloads/controllers/statefulset.md`, section: *StatefulSets > Pod Identity*
  > [StatefulSets > Pod Identity]
  > StatefulSet Pods have a unique identity that consists of an ordinal, a
  > stable network identity, and stable storage. The identity sticks to the Pod,
  > regardless of which node it's (re)scheduled on.
  > [StatefulSets > Pod Identity > Ordinal Index]
  > For a StatefulSet with N replicas, each Pod in the StatefulSet
  > will be assigned an integer ordinal, that is unique over the Set. By default,
  > pods will be assigned ordinals from 0 up through N-1. The StatefulSet controller
  > will also add a pod label with this index: `apps.kubernetes.io/pod-index`.
  > [StatefulSets > Pod Identity > Start ordinal]
  > `.spec.ordinals` is an optional field that allows you to configure the integer
  > ordinals assigned to each Pod. It defaults to nil. Within the field, you can
  > configure the following options:
  > * `.spec.ordinals.start`: If the `.spec.ordinals.start` field is set, Pods will
  >   be assigned ordinals from `.spec.ordinals.start` up through
  >   `.spec.ordinals.start + .spec.replicas - 1`.
  > [StatefulSets > Pod Identity > Stable Network ID]
  > Each Pod in a StatefulSet derives its hostname from the name of the StatefulSet
  > and the ordinal of the Pod. The pattern for the constructed hostname
  > is `$(statefulset name)-$(ordinal)`. The example above will create three Pods
  > named `web-0,web-1,web-2`.
  > A StatefulSet can use a Headless Service
  > to control the domain of its Pods. The domain managed by this Service takes the form:
  > `$(service name).$(namespace).svc.cluster.local`, where "cluster.local" is the
  > cluster domain.
  > As each Pod is created, it gets a matching DNS subdomain, taking the form:
  > `$(podname).$(governing service domain)`, where the governing service is defined
  > by the `serviceName` field on the StatefulSet.
  > Depending on how DNS is configured in your cluster, you may not be able to look up the DNS
  > name for a newly-run Pod immediately. This behavior can occur when other clients in the
  > cluster have already sent queries for the hostname of the Pod before it was created.
  > Negative caching (normal in DNS) means that the results of previous failed lookups are
  > remembered and reused, even after the Pod is running, for at least a few seconds.
  > If you need to discover Pods promptly after they are created, you have a few options:
  > If you need to discover Pods promptly after they are created, you have a few options:
  > - Query the Kubernetes API directly (for example, using a watch) rather than relying on DNS lookups.
  > - Decrease the time of caching in your Kubernetes DNS provider (typically this means editing the
  >   config map for CoreDNS, which currently caches for 30 seconds).
  > As mentioned in the limitations section, you are responsible for
  > creating the Headless Service
  > responsible for the network identity of the pods.
  > Here are some examples of choices for Cluster Domain, Service name,
  > StatefulSet name, and how that affects the DNS names for the StatefulSet's Pods.
  > Here are some examples of choices for Cluster Domain, Service name,
  > StatefulSet name, and how that affects the DNS names for the StatefulSet's Pods.
  > Cluster Domain | Service (ns/name) | StatefulSet (ns/name)  | StatefulSet Domain  | Pod DNS | Pod Hostname |
  > -------------- | ----------------- | ----------------- | -------------- | ------- | ------------ |
  >  cluster.local | default/nginx     | default/web       | nginx.default.svc.cluster.local | web-{0..N-1}.nginx.default.svc.cluster.local | web-{0..N-1} |
  >  cluster.local | foo/nginx         | foo/web           | nginx.foo.svc.cluster.local     | web-{0..N-1}.nginx.foo.svc.cluster.local     | web-{0..N-1} |
  >  kube.local    | foo/nginx         | foo/web           | nginx.foo.svc.kube.local        | web-{0..N-1}.nginx.foo.svc.kube.local        | web-{0..N-1} |
  > Cluster Domain will be set to `cluster.local` unless
  > otherwise configured.
  > [StatefulSets > Pod Identity > Stable Storage]
  > For each VolumeClaimTemplate entry defined in a StatefulSet, each Pod receives one
  > PersistentVolumeClaim. In the nginx example above, each Pod receives a single PersistentVolume
  > with a StorageClass of `my-storage-class` and 1 GiB of provisioned storage. If no StorageClass
  > is specified, then the default StorageClass will be used. When a Pod is (re)scheduled
  > onto a node, its `volumeMounts` mount the PersistentVolumes associated with its
  > PersistentVolume Claims. Note that, the PersistentVolumes associated with the
  > Pods' PersistentVolume Claims are not deleted when the Pods, or StatefulSet are deleted.
  > This must be done manually.
  > [StatefulSets > Pod Identity > Pod Name Label]
  > When the StatefulSet controller creates a Pod,
  > it adds a label, `statefulset.kubernetes.io/pod-name`, that is set to the name of
  > the Pod. This label allows you to attach a Service to a specific Pod in
  > the StatefulSet.
  > [StatefulSets > Pod Identity > Pod index label]
  > When the StatefulSet controller creates a Pod,
  > the new Pod is labelled with `apps.kubernetes.io/pod-index`. The value of this label is the ordinal index of
  > the Pod. This label allows you to route traffic to a particular pod index, filter logs/metrics
  > using the pod index label, and more. Note the feature gate `PodIndexLabel` is enabled and locked by default for this
  > feature, in order to disable it, users will have to use server emulated version v1.31.

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): removed the unsupported comparison with Deployments | human review (Youssef Zemzem, 2026-11-07): qualified the claim about databases | human review 2 (Youssef Zemzem, 2026-11-07): removed the database generalisation; question made general; id renamed from statefulset-database

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `emptydir-scratch`

**Question** (en, task): How do I give a pod scratch storage that is deleted when the pod goes away?

**Reference answer:** Use an `emptyDir` volume: it exists as long as the Pod runs on the node, survives container restarts, and is deleted when the Pod is removed.

**Relevant documentation:**
- `tasks/configure-pod-container/configure-volume-storage.md`, section: *Configure a Pod to Use a Volume for Storage > Configure a volume for a Pod*
  > [Configure a Pod to Use a Volume for Storage > Configure a volume for a Pod]
  > In this exercise, you create a Pod that runs one Container. This Pod has a
  > Volume of type
  > emptyDir
  > that lasts for the life of the Pod, even if the Container terminates and
  > restarts. Here is the configuration file for the Pod:
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
  > 1. Create the Pod:
  >    ```shell
  >    kubectl apply -f https://k8s.io/examples/pods/storage/redis.yaml
  >    ```
  > 1. Verify that the Pod's Container is running, and then watch for changes to
  >    the Pod:
  >    ```shell
  >    kubectl get pod redis --watch
  >    ```
  >    The output looks like this:
  >    ```console
  >    NAME      READY     STATUS    RESTARTS   AGE
  >    redis     1/1       Running   0          13s
  >    ```
  > 1. In another terminal, get a shell to the running Container:
  >    ```shell
  >    kubectl exec -it redis -- /bin/bash
  >    ```
  > 1. In your shell, go to `/data/redis`, and then create a file:
  >    ```shell
  >    root@redis:/data# cd /data/redis/
  >    root@redis:/data/redis# echo Hello > test-file
  >    ```
  >    ```shell
  >    root@redis:/data# cd /data/redis/
  >    root@redis:/data/redis# echo Hello > test-file
  >    ```
  > 1. In your shell, list the running processes:
  >    ```shell
  >    root@redis:/data/redis# apt-get update
  >    root@redis:/data/redis# apt-get install procps
  >    root@redis:/data/redis# ps aux
  >    ```
  >    The output is similar to this:
  >    ```console
  >    USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
  >    redis        1  0.1  0.1  33308  3828 ?        Ssl  00:46   0:00 redis-server *:6379
  >    root        12  0.0  0.0  20228  3020 ?        Ss   00:47   0:00 /bin/bash
  >    root        15  0.0  0.0  17500  2072 ?        R+   00:48   0:00 ps aux
  >    ```
  > 1. In your shell, kill the Redis process:
  >    ```shell
  >    root@redis:/data/redis# kill <pid>
  >    ```
  >    where `<pid>` is the Redis process ID (PID).
  > 1. In your original terminal, watch for changes to the Redis Pod. Eventually,
  >    you will see something like this:
  >    ```console
  >    NAME      READY     STATUS     RESTARTS   AGE
  >    redis     1/1       Running    0          13s
  >    redis     0/1       Completed  0         6m
  >    redis     1/1       Running    1         6m
  >    ```
  > At this point, the Container has terminated and restarted. This is because the
  > Redis Pod has a
  > restartPolicy
  > of `Always`.
  > 1. Get a shell into the restarted Container:
  >    ```shell
  >    kubectl exec -it redis -- /bin/bash
  >    ```
  > 1. In your shell, go to `/data/redis`, and verify that `test-file` is still there.
  >    ```shell
  >    root@redis:/data/redis# cd /data/redis/
  >    root@redis:/data/redis# ls
  >    test-file
  >    ```
  > 1. Delete the Pod that you created for this exercise:
  >    ```shell
  >    kubectl delete pod redis
  >    ```
  > ##
  > - See Volume.
  > - See Pod.
  > - In addition to the local disk storage provided by `emptyDir`, Kubernetes
  >   supports many different network-attached storage solutions, including PD on
  >   GCE and EBS on EC2, which are preferred for critical data and will handle
  >   details such as mounting and unmounting the devices on the nodes. See
  >   Volumes for more details.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `pv-mount-steps`

**Question** (en, task): What are the steps to mount a PersistentVolume into a pod?

**Reference answer:** Create a PersistentVolume, create a PersistentVolumeClaim that binds to it, then create a Pod that uses the claim as a volume.

**Relevant documentation:**
- `tasks/configure-pod-container/configure-persistent-volume-storage.md`, section: *Configure a Pod to Use a PersistentVolume for Storage > Create a PersistentVolume*
  > [Configure a Pod to Use a PersistentVolume for Storage > Create a PersistentVolume]
  > In this exercise, you create a *hostPath* PersistentVolume. Kubernetes supports
  > hostPath for development and testing on a single-node cluster. A hostPath
  > PersistentVolume uses a file or directory on the Node to emulate network-attached storage.
  > In a production cluster, you would not use hostPath. Instead a cluster administrator
  > would provision a network resource like a Google Compute Engine persistent disk,
  > an NFS share, or an Amazon Elastic Block Store volume. Cluster administrators can also
  > use StorageClasses
  > to set up
  > dynamic provisioning.
  > Here is the configuration file for the hostPath PersistentVolume:
  > Example file `pods/storage/pv-volume.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: PersistentVolume
  > metadata:
  >   name: task-pv-volume
  >   labels:
  >     type: local
  > spec:
  >   storageClassName: manual
  >   capacity:
  >     storage: 10Gi
  >   accessModes:
  >     - ReadWriteOnce
  >   hostPath:
  >     path: "/mnt/data"
  > ```
  > The configuration file specifies that the volume is at `/mnt/data` on the
  > cluster's Node. The configuration also specifies a size of 10 gibibytes and
  > an access mode of `ReadWriteOnce`, which means the volume can be mounted as
  > read-write by a single Node. It defines the StorageClass name
  > `manual` for the PersistentVolume, which will be used to bind
  > PersistentVolumeClaim requests to this PersistentVolume.
  > This example uses the `ReadWriteOnce` access mode, for simplicity. For
  > production use, the Kubernetes project recommends using the `ReadWriteOncePod`
  > access mode instead.
  > Create the PersistentVolume:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/storage/pv-volume.yaml
  > ```
  > View information about the PersistentVolume:
  > ```shell
  > kubectl get pv task-pv-volume
  > ```
  > The output shows that the PersistentVolume has a `STATUS` of `Available`. This
  > means it has not yet been bound to a PersistentVolumeClaim.
  > ```
  > NAME             CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS      CLAIM     STORAGECLASS   REASON    AGE
  > task-pv-volume   10Gi       RWO           Retain          Available             manual                   4s
  > ```
  > [Configure a Pod to Use a PersistentVolume for Storage > Create a PersistentVolumeClaim]
  > The next step is to create a PersistentVolumeClaim. Pods use PersistentVolumeClaims
  > to request physical storage. In this exercise, you create a PersistentVolumeClaim
  > that requests a volume of at least three gibibytes that can provide read-write
  > access for at most one Node at a time.
  > Here is the configuration file for the PersistentVolumeClaim:
  > Example file `pods/storage/pv-claim.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: PersistentVolumeClaim
  > metadata:
  >   name: task-pv-claim
  > spec:
  >   storageClassName: manual
  >   accessModes:
  >     - ReadWriteOnce
  >   resources:
  >     requests:
  >       storage: 3Gi
  > ```
  > Create the PersistentVolumeClaim:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/storage/pv-claim.yaml
  > ```
  > After you create the PersistentVolumeClaim, the Kubernetes control plane looks
  > for a PersistentVolume that satisfies the claim's requirements. If the control
  > plane finds a suitable PersistentVolume with the same StorageClass, it binds the
  > claim to the volume.
  > Look again at the PersistentVolume:
  > ```shell
  > kubectl get pv task-pv-volume
  > ```
  > Now the output shows a `STATUS` of `Bound`.
  > Now the output shows a `STATUS` of `Bound`.
  > ```
  > NAME             CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM                   STORAGECLASS   REASON    AGE
  > task-pv-volume   10Gi       RWO           Retain          Bound     default/task-pv-claim   manual                   2m
  > ```
  > Look at the PersistentVolumeClaim:
  > ```shell
  > kubectl get pvc task-pv-claim
  > ```
  > The output shows that the PersistentVolumeClaim is bound to your PersistentVolume,
  > `task-pv-volume`.
  > ```
  > NAME            STATUS    VOLUME           CAPACITY   ACCESSMODES   STORAGECLASS   AGE
  > task-pv-claim   Bound     task-pv-volume   10Gi       RWO           manual         30s
  > ```
- `tasks/configure-pod-container/configure-persistent-volume-storage.md`, section: *Configure a Pod to Use a PersistentVolume for Storage > Create a PersistentVolumeClaim*
  > [Configure a Pod to Use a PersistentVolume for Storage > Create a PersistentVolumeClaim]
  > The next step is to create a PersistentVolumeClaim. Pods use PersistentVolumeClaims
  > to request physical storage. In this exercise, you create a PersistentVolumeClaim
  > that requests a volume of at least three gibibytes that can provide read-write
  > access for at most one Node at a time.
  > Here is the configuration file for the PersistentVolumeClaim:
  > Example file `pods/storage/pv-claim.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: PersistentVolumeClaim
  > metadata:
  >   name: task-pv-claim
  > spec:
  >   storageClassName: manual
  >   accessModes:
  >     - ReadWriteOnce
  >   resources:
  >     requests:
  >       storage: 3Gi
  > ```
  > Create the PersistentVolumeClaim:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/storage/pv-claim.yaml
  > ```
  > After you create the PersistentVolumeClaim, the Kubernetes control plane looks
  > for a PersistentVolume that satisfies the claim's requirements. If the control
  > plane finds a suitable PersistentVolume with the same StorageClass, it binds the
  > claim to the volume.
  > Look again at the PersistentVolume:
  > ```shell
  > kubectl get pv task-pv-volume
  > ```
  > Now the output shows a `STATUS` of `Bound`.
  > Now the output shows a `STATUS` of `Bound`.
  > ```
  > NAME             CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM                   STORAGECLASS   REASON    AGE
  > task-pv-volume   10Gi       RWO           Retain          Bound     default/task-pv-claim   manual                   2m
  > ```
  > Look at the PersistentVolumeClaim:
  > ```shell
  > kubectl get pvc task-pv-claim
  > ```
  > The output shows that the PersistentVolumeClaim is bound to your PersistentVolume,
  > `task-pv-volume`.
  > ```
  > NAME            STATUS    VOLUME           CAPACITY   ACCESSMODES   STORAGECLASS   AGE
  > task-pv-claim   Bound     task-pv-volume   10Gi       RWO           manual         30s
  > ```
- `tasks/configure-pod-container/configure-persistent-volume-storage.md`, section: *Configure a Pod to Use a PersistentVolume for Storage > Create a Pod*
  > [Configure a Pod to Use a PersistentVolume for Storage > Create a Pod]
  > The next step is to create a Pod that uses your PersistentVolumeClaim as a volume.
  > Here is the configuration file for the Pod:
  > Example file `pods/storage/pv-pod.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: task-pv-pod
  > spec:
  >   volumes:
  >     - name: task-pv-storage
  >       persistentVolumeClaim:
  >         claimName: task-pv-claim
  >   containers:
  >     - name: task-pv-container
  >       image: nginx
  >       ports:
  >         - containerPort: 80
  >           name: "http-server"
  >       volumeMounts:
  >         - mountPath: "/usr/share/nginx/html"
  >           name: task-pv-storage
  > ```
  > Notice that the Pod's configuration file specifies a PersistentVolumeClaim, but
  > it does not specify a PersistentVolume. From the Pod's point of view, the claim
  > is a volume.
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/storage/pv-pod.yaml
  > ```
  > Verify that the container in the Pod is running:
  > ```shell
  > kubectl get pod task-pv-pod
  > ```
  > Get a shell to the container running in your Pod:
  > ```shell
  > kubectl exec -it task-pv-pod -- /bin/bash
  > ```
  > In your shell, verify that nginx is serving the `index.html` file from the
  > hostPath volume:
  > In your shell, verify that nginx is serving the `index.html` file from the
  > hostPath volume:
  > ```shell
  > # Be sure to run these 3 commands inside the root shell that comes from
  > # running "kubectl exec" in the previous step
  > apt update
  > apt install curl
  > curl http://localhost/
  > ```
  > The output shows the text that you wrote to the `index.html` file on the
  > hostPath volume:
  > ```
  > Hello from Kubernetes storage
  > ```
  > If you see that message, you have successfully configured a Pod to
  > use storage from a PersistentVolumeClaim.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `run-as-user`

**Question** (en, task): How do I make the processes in a container run as a specific non-root user?

**Reference answer:** Set `securityContext.runAsUser` (and optionally `runAsGroup`) at Pod level or container level; container-level settings override Pod-level ones.

**Relevant documentation:**
- `tasks/configure-pod-container/security-context.md`, section: *Configure a Security Context for a Pod or Container > Set the security context for a Pod*
  > [Configure a Security Context for a Pod or Container > Set the security context for a Pod]
  > To specify security settings for a Pod, include the `securityContext` field
  > in the Pod specification. The `securityContext` field is a
  > PodSecurityContext object.
  > The security settings that you specify for a Pod apply to all Containers in the Pod.
  > Here is a configuration file for a Pod that has a `securityContext` and an `emptyDir` volume:
  > Example file `pods/security/security-context.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: security-context-demo
  > spec:
  >   securityContext:
  >     runAsUser: 1000
  >     runAsGroup: 3000
  >     fsGroup: 2000
  >     supplementalGroups: [4000]
  >   volumes:
  >   - name: sec-ctx-vol
  >     emptyDir: {}
  >   containers:
  >   - name: sec-ctx-demo
  >     image: busybox:1.28
  >     command: [ "sh", "-c", "sleep 1h" ]
  >     volumeMounts:
  >     - name: sec-ctx-vol
  >       mountPath: /data/demo
  >     securityContext:
  >       allowPrivilegeEscalation: false
  > ```
  > In the configuration file, the `runAsUser` field specifies that for any Containers in
  > the Pod, all processes run with user ID 1000. The `runAsGroup` field specifies the primary group ID of 3000 for
  > all processes within any containers of the Pod. If this field is omitted, the primary group ID of the containers
  > will be root(0). Any files created will also be owned by user 1000 and group 3000 when `runAsGroup` is specified.
  > Since `fsGroup` field is specified, all processes of the container are also part of the supplementary group ID 2000.
  > The owner for volume `/data/demo` and any files created in that volume will be Group ID 2000.
  > Additionally, when the `supplementalGroups` field is specified, all processes of the container are also part of the
  > specified groups. If this field is omitted, it means empty.
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/security/security-context.yaml
  > ```
  > Verify that the Pod's Container is running:
  > ```shell
  > kubectl get pod security-context-demo
  > ```
  > Get a shell to the running Container:
  > ```shell
  > kubectl exec -it security-context-demo -- sh
  > ```
  > In your shell, list the running processes:
  > ```shell
  > ps
  > ```
  > ```shell
  > ps
  > ```
  > The output shows that the processes are running as user 1000, which is the value of `runAsUser`:
  > ```none
  > PID   USER     TIME  COMMAND
  >     1 1000      0:00 sleep 1h
  >     6 1000      0:00 sh
  > ...
  > ```
  > In your shell, navigate to `/data`, and list the one directory:
  > ```shell
  > cd /data
  > ls -l
  > ```
  > The output shows that the `/data/demo` directory has group ID 2000, which is
  > the value of `fsGroup`.
  > ```none
  > drwxrwsrwx 2 root 2000 4096 Jun  6 20:08 demo
  > ```
  > In your shell, navigate to `/data/demo`, and create a file:
  > ```shell
  > cd demo
  > echo hello > testfile
  > ```
  > List the file in the `/data/demo` directory:
  > ```shell
  > ls -l
  > ```
  > The output shows that `testfile` has group ID 2000, which is the value of `fsGroup`.
  > ```none
  > -rw-r--r-- 1 1000 2000 6 Jun  6 20:08 testfile
  > ```
  > Run the following command:
  > ```shell
  > id
  > ```
  > The output is similar to this:
  > ```none
  > uid=1000 gid=3000 groups=2000,3000,4000
  > ```
  > ```none
  > uid=1000 gid=3000 groups=2000,3000,4000
  > ```
  > From the output, you can see that `gid` is 3000 which is same as the `runAsGroup` field.
  > If the `runAsGroup` was omitted, the `gid` would remain as 0 (root) and the process will
  > be able to interact with files that are owned by the root(0) group and groups that have
  > the required group permissions for the root (0) group. You can also see that `groups`
  > contains the group IDs which are specified by `fsGroup` and `supplementalGroups`,
  > in addition to `gid`.
  > Exit your shell:
  > ```shell
  > exit
  > ```
  > [Configure a Security Context for a Pod or Container > Set the security context for a Pod > Implicit group memberships defined in `/etc/group` in the container image]
  > By default, kubernetes merges group information from the Pod with information defined in `/etc/group` in the container image.
  > Example file `pods/security/security-context-5.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: security-context-demo
  > spec:
  >   securityContext:
  >     runAsUser: 1000
  >     runAsGroup: 3000
  >     supplementalGroups: [4000]
  >   containers:
  >   - name: sec-ctx-demo
  >     image: registry.k8s.io/e2e-test-images/agnhost:2.45
  >     command: [ "sh", "-c", "sleep 1h" ]
  >     securityContext:
  >       allowPrivilegeEscalation: false
  > ```
  > This Pod security context contains `runAsUser`, `runAsGroup` and `supplementalGroups`.
  > However, you can see that the actual supplementary groups attached to the container process
  > will include group IDs which come from `/etc/group` in the container image.
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/security/security-context-5.yaml
  > ```
  > Verify that the Pod's Container is running:
  > ```shell
  > kubectl get pod security-context-demo
  > ```
  > Get a shell to the running Container:
  > ```shell
  > kubectl exec -it security-context-demo -- sh
  > ```
  > Check the process identity:
  > ```shell
  > $ id
  > ```
  > The output is similar to this:
  > The output is similar to this:
  > ```none
  > uid=1000 gid=3000 groups=3000,4000,50000
  > ```
  > You can see that `groups` includes group ID `50000`. This is because the user (`uid=1000`),
  > which is defined in the image, belongs to the group (`gid=50000`), which is defined in `/etc/group`
  > inside the container image.
  > Check the `/etc/group` in the container image:
  > ```shell
  > $ cat /etc/group
  > ```
  > You can see that uid `1000` belongs to group `50000`.
  > ```none
  > ...
  > user-defined-in-image:x:1000:
  > group-defined-in-image:x:50000:user-defined-in-image
  > ```
  > Exit your shell:
  > ```shell
  > exit
  > ```
  > _Implicitly merged_ supplementary groups may cause security problems particularly when accessing
  > the volumes (see kubernetes/kubernetes#112879 for details).
  > If you want to avoid this. Please see the below section.
- `tasks/configure-pod-container/security-context.md`, section: *Configure a Security Context for a Pod or Container > Set the security context for a Container*
  > [Configure a Security Context for a Pod or Container > Set the security context for a Container]
  > To specify security settings for a Container, include the `securityContext` field
  > in the Container manifest. The `securityContext` field is a
  > SecurityContext object.
  > Security settings that you specify for a Container apply only to
  > the individual Container, and they override settings made at the Pod level when
  > there is overlap. Container settings do not affect the Pod's Volumes.
  > Here is the configuration file for a Pod that has one Container. Both the Pod
  > and the Container have a `securityContext` field:
  > Example file `pods/security/security-context-2.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: security-context-demo-2
  > spec:
  >   securityContext:
  >     runAsUser: 1000
  >   containers:
  >   - name: sec-ctx-demo-2
  >     image: gcr.io/google-samples/hello-app:2.0
  >     securityContext:
  >       runAsUser: 2000
  >       allowPrivilegeEscalation: false
  > ```
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/security/security-context-2.yaml
  > ```
  > Verify that the Pod's Container is running:
  > ```shell
  > kubectl get pod security-context-demo-2
  > ```
  > Get a shell into the running Container:
  > ```shell
  > kubectl exec -it security-context-demo-2 -- sh
  > ```
  > ```shell
  > kubectl exec -it security-context-demo-2 -- sh
  > ```
  > In your shell, list the running processes:
  > ```shell
  > ps aux
  > ```
  > The output shows that the processes are running as user 2000. This is the value
  > of `runAsUser` specified for the Container. It overrides the value 1000 that is
  > specified for the Pod.
  > ```
  > USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
  > 2000         1  0.0  0.0   4336   764 ?        Ss   20:36   0:00 /bin/sh -c node server.js
  > 2000         8  0.1  0.5 772124 22604 ?        Sl   20:36   0:00 node server.js
  > ...
  > ```
  > Exit your shell:
  > ```shell
  > exit
  > ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The excerpt demonstrates runAsUser at both Pod and container level, but demonstrates runAsGroup only at Pod level. Clarify this distinction or provide documentation explicitly showing container-level runAsGroup.
---

### `linux-capabilities`

**Question** (en, task): How do I add or remove Linux capabilities for a container?

**Reference answer:** Use `securityContext.capabilities` in the container spec and list capabilities to `add` (e.g. `NET_ADMIN`, `SYS_TIME`).

**Relevant documentation:**
- `tasks/configure-pod-container/security-context.md`, section: *Configure a Security Context for a Pod or Container > Set capabilities for a Container*
  > [Configure a Security Context for a Pod or Container > Set capabilities for a Container]
  > With Linux capabilities,
  > you can grant certain privileges to a process without granting all the privileges
  > of the root user. To add or remove Linux capabilities for a Container, include the
  > `capabilities` field in the `securityContext` section of the Container manifest.
  > First, see what happens when you don't include a `capabilities` field.
  > Here is configuration file that does not add or remove any Container capabilities:
  > Example file `pods/security/security-context-3.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: security-context-demo-3
  > spec:
  >   containers:
  >   - name: sec-ctx-3
  >     image: gcr.io/google-samples/hello-app:2.0
  > ```
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/security/security-context-3.yaml
  > ```
  > Verify that the Pod's Container is running:
  > ```shell
  > kubectl get pod security-context-demo-3
  > ```
  > Get a shell into the running Container:
  > ```shell
  > kubectl exec -it security-context-demo-3 -- sh
  > ```
  > In your shell, list the running processes:
  > ```shell
  > ps aux
  > ```
  > The output shows the process IDs (PIDs) for the Container:
  > The output shows the process IDs (PIDs) for the Container:
  > ```
  > USER  PID %CPU %MEM    VSZ   RSS TTY   STAT START   TIME COMMAND
  > root    1  0.0  0.0   4336   796 ?     Ss   18:17   0:00 /bin/sh -c node server.js
  > root    5  0.1  0.5 772124 22700 ?     Sl   18:17   0:00 node server.js
  > ```
  > In your shell, view the status for process 1:
  > ```shell
  > cd /proc/1
  > cat status
  > ```
  > The output shows the capabilities bitmap for the process:
  > ```
  > ...
  > CapPrm:	00000000a80425fb
  > CapEff:	00000000a80425fb
  > ...
  > ```
  > Make a note of the capabilities bitmap, and then exit your shell:
  > ```shell
  > exit
  > ```
  > Next, run a Container that is the same as the preceding container, except
  > that it has additional capabilities set.
  > Here is the configuration file for a Pod that runs one Container. The configuration
  > adds the `CAP_NET_ADMIN` and `CAP_SYS_TIME` capabilities:
  > Example file `pods/security/security-context-4.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: security-context-demo-4
  > spec:
  >   containers:
  >   - name: sec-ctx-4
  >     image: gcr.io/google-samples/hello-app:2.0
  >     securityContext:
  >       capabilities:
  >         add: ["NET_ADMIN", "SYS_TIME"]
  > ```
  > Create the Pod:
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/security/security-context-4.yaml
  > ```
  > Get a shell into the running Container:
  > ```shell
  > kubectl exec -it security-context-demo-4 -- sh
  > ```
  > In your shell, view the capabilities for process 1:
  > ```shell
  > cd /proc/1
  > cat status
  > ```
  > The output shows capabilities bitmap for the process:
  > ```
  > ...
  > CapPrm:	00000000aa0435fb
  > CapEff:	00000000aa0435fb
  > ...
  > ```
  > Compare the capabilities of the two Containers:
  > ```
  > 00000000a80425fb
  > 00000000aa0435fb
  > ```
  > In the capability bitmap of the first container, bits 12 and 25 are clear. In the second container,
  > bits 12 and 25 are set. Bit 12 is `CAP_NET_ADMIN`, and bit 25 is `CAP_SYS_TIME`.
  > See capability.h
  > for definitions of the capability constants.
  > Linux capability constants have the form `CAP_XXX`.
  > But when you list capabilities in your container manifest, you must
  > omit the `CAP_` portion of the constant.
  > For example, to add `CAP_SYS_TIME`, include `SYS_TIME` in your list of capabilities.

*Drafting note:* golden v2 draft (2026-11-07) | self-check: aligned with the referenced text

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The question asks how to add or remove Linux capabilities, but the reference answer only explains adding them. Include the drop field for removing capabilities, or narrow the question to adding capabilities only.
---

### `private-registry`

**Question** (en, task): How can a pod pull an image from a private registry that needs a login?

**Reference answer:** Create a docker-registry Secret (e.g. `kubectl create secret docker-registry regcred ...`) and reference it in the Pod's `imagePullSecrets`.

**Relevant documentation:**
- `tasks/configure-pod-container/pull-image-private-registry.md`, section: *Pull an Image from a Private Registry > Create a Secret by providing credentials on the command line*
  > [Pull an Image from a Private Registry > Create a Secret by providing credentials on the command line]
  > Create this Secret, naming it `regcred`:
  > ```shell
  > kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
  > ```
  > where:
  > * `<your-registry-server>` is your Private Docker Registry FQDN.
  >   Use `https://index.docker.io/v1/` for DockerHub.
  > * `<your-name>` is your Docker username.
  > * `<your-pword>` is your Docker password.
  > * `<your-email>` is your Docker email.
  > You have successfully set your Docker credentials in the cluster as a Secret called `regcred`.
  > Typing secrets on the command line may store them in your shell history unprotected, and
  > those secrets might also be visible to other users on your PC during the time that
  > `kubectl` is running.
- `tasks/configure-pod-container/pull-image-private-registry.md`, section: *Pull an Image from a Private Registry > Create a Pod that uses your Secret*
  > [Pull an Image from a Private Registry > Create a Pod that uses your Secret]
  > Here is a manifest for an example Pod that needs access to your Docker credentials in `regcred`:
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
  > Download the above file onto your computer:
  > ```shell
  > curl -L -o my-private-reg-pod.yaml https://k8s.io/examples/pods/private-reg-pod.yaml
  > ```
  > In file `my-private-reg-pod.yaml`, replace `<your-private-image>` with the path to an image in a private registry such as:
  > ```none
  > your.private.registry.example.com/janedoe/jdoe-private:v1
  > ```
  > To pull the image from the private registry, Kubernetes needs credentials.
  > The `imagePullSecrets` field in the configuration file specifies that
  > Kubernetes should get the credentials from a Secret named `regcred`.
  > Create a Pod that uses your Secret, and verify that the Pod is running:
  > ```shell
  > kubectl apply -f my-private-reg-pod.yaml
  > kubectl get pod private-reg
  > ```
  > ```shell
  > kubectl apply -f my-private-reg-pod.yaml
  > kubectl get pod private-reg
  > ```
  > To use image pull secrets for a Pod (or a Deployment, or other object that
  > has a pod template that you are using), you need to make sure that the appropriate
  > Secret does exist in the right namespace. The namespace to use is the same
  > namespace where you defined the Pod.
  > Also, in case the Pod fails to start with the status `ImagePullBackOff`, view the Pod events:
  > ```shell
  > kubectl describe pod private-reg
  > ```
  > If you then see an event with the reason set to `FailedToRetrieveImagePullSecret`,
  > Kubernetes can't find a Secret with name (`regcred`, in this example).
  > Make sure that the Secret you have specified exists, and that its name is spelled properly.
  > ```shell
  > Events:
  >   ...  Reason                           ...  Message
  >        ------                                -------
  >   ...  FailedToRetrieveImagePullSecret  ...  Unable to retrieve some image pull secrets (<regcred>); attempting to pull the image may not succeed.
  > ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `secret-as-files`

**Question** (en, task): How do I give a container access to a Secret as files?

**Reference answer:** Mount the Secret as a volume; each key becomes a file under the volume's `mountPath`.

**Relevant documentation:**
- `tasks/inject-data-application/distribute-credentials-secure.md`, section: *Distribute Credentials Securely Using Secrets > Create a Pod that has access to the secret data through a Volume*
  > [Distribute Credentials Securely Using Secrets > Create a Pod that has access to the secret data through a Volume]
  > Here is a configuration file you can use to create a Pod:
  > Example file `pods/inject/secret-pod.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: secret-test-pod
  > spec:
  >   containers:
  >     - name: test-container
  >       image: nginx
  >       volumeMounts:
  >         # name must match the volume name below
  >         - name: secret-volume
  >           mountPath: /etc/secret-volume
  >           readOnly: true
  >   # The secret data is exposed to Containers in the Pod through a Volume.
  >   volumes:
  >     - name: secret-volume
  >       secret:
  >         secretName: test-secret
  > ```
  > 1. Create the Pod:
  >    ```shell
  >    kubectl apply -f https://k8s.io/examples/pods/inject/secret-pod.yaml
  >    ```
  > 1. Verify that your Pod is running:
  >    ```shell
  >    kubectl get pod secret-test-pod
  >    ```
  >    Output:
  >    ```
  >    NAME              READY     STATUS    RESTARTS   AGE
  >    secret-test-pod   1/1       Running   0          42m
  >    ```
  > 1. Get a shell into the Container that is running in your Pod:
  >    ```shell
  >    kubectl exec -i -t secret-test-pod -- /bin/bash
  >    ```
  > 1. The secret data is exposed to the Container through a Volume mounted under
  >    `/etc/secret-volume`.
  > 1. The secret data is exposed to the Container through a Volume mounted under
  >    `/etc/secret-volume`.
  >    In your shell, list the files in the `/etc/secret-volume` directory:
  >    ```shell
  >    # Run this in the shell inside the container
  >    ls /etc/secret-volume
  >    ```
  >    The output shows two files, one for each piece of secret data:
  >    ```
  >    password username
  >    ```
  > 1. In your shell, display the contents of the `username` and `password` files:
  >    ```shell
  >    # Run this in the shell inside the container
  >    echo "$( cat /etc/secret-volume/username )"
  >    echo "$( cat /etc/secret-volume/password )"
  >    ```
  >    The output is your username and password:
  >    ```
  >    my-app
  >    39528$vdg7Jb
  >    ```
  > Modify your image or command line so that the program looks for files in the
  > `mountPath` directory. Each key in the Secret `data` map becomes a file name
  > in this directory.
  > [Distribute Credentials Securely Using Secrets > Create a Pod that has access to the secret data through a Volume > Project Secret keys to specific file paths]
  > You can also control the paths within the volume where Secret keys are projected. Use the
  > `.spec.volumes[].secret.items` field to change the target path of each key:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: mypod
  > spec:
  >   containers:
  >   - name: mypod
  >     image: redis
  >     volumeMounts:
  >     - name: foo
  >       mountPath: "/etc/foo"
  >       readOnly: true
  >   volumes:
  >   - name: foo
  >     secret:
  >       secretName: mysecret
  >       items:
  >       - key: username
  >         path: my-group/my-username
  > ```
  > When you deploy this Pod, the following happens:
  > - The `username` key from `mysecret` is available to the container at the path
  >   `/etc/foo/my-group/my-username` instead of at `/etc/foo/username`.
  > - The `password` key from that Secret object is not projected.
  > If you list keys explicitly using `.spec.volumes[].secret.items`, consider the
  > following:
  > - Only keys specified in `items` are projected.
  > - To consume all keys from the Secret, all of them must be listed in the
  >   `items` field.
  > - All listed keys must exist in the corresponding Secret. Otherwise, the volume
  >   is not created.
  > [Distribute Credentials Securely Using Secrets > Create a Pod that has access to the secret data through a Volume > Set POSIX permissions for Secret keys]
  > You can set the POSIX file access permission bits for a single Secret key.
  > If you don't specify any permissions, `0644` is used by default.
  > You can also set a default POSIX file mode for the entire Secret volume, and
  > you can override per key if needed.
  > For example, you can specify a default mode like this:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: mypod
  > spec:
  >   containers:
  >   - name: mypod
  >     image: redis
  >     volumeMounts:
  >     - name: foo
  >       mountPath: "/etc/foo"
  >   volumes:
  >   - name: foo
  >     secret:
  >       secretName: mysecret
  >       defaultMode: 0400
  > ```
  > The Secret is mounted on `/etc/foo`; all the files created by the
  > secret volume mount have permission `0400`.
  > If you're defining a Pod or a Pod template using JSON, beware that the JSON
  > specification doesn't support octal literals for numbers because JSON considers
  > `0400` to be the _decimal_ value `400`. In JSON, use decimal values for the
  > `defaultMode` instead. If you're writing YAML, you can write the `defaultMode`
  > in octal.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `secret-env-var`

**Question** (en, task): How do I expose a value from a Secret as an environment variable?

**Reference answer:** In the container's `env`, use `valueFrom.secretKeyRef` with the Secret's name and key.

**Relevant documentation:**
- `tasks/inject-data-application/distribute-credentials-secure.md`, section: *Distribute Credentials Securely Using Secrets > Define container environment variables using Secret data*
  > [Distribute Credentials Securely Using Secrets > Define container environment variables using Secret data]
  > You can consume the data in Secrets as environment variables in your
  > containers.
  > If a container already consumes a Secret in an environment variable,
  > a Secret update will not be seen by the container unless it is
  > restarted. There are third party solutions for triggering restarts when
  > secrets change.
  > [Distribute Credentials Securely Using Secrets > Define container environment variables using Secret data > Define a container environment variable with data from a single Secret]
  > - Define an environment variable as a key-value pair in a Secret:
  >   ```shell
  >   kubectl create secret generic backend-user --from-literal=backend-username='backend-admin'
  >   ```
  > - Assign the `backend-username` value defined in the Secret to the `SECRET_USERNAME` environment variable in the Pod specification.
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
  > - Create the Pod:
  >   ```shell
  >   kubectl create -f https://k8s.io/examples/pods/inject/pod-single-secret-env-variable.yaml
  >   ```
  > - In your shell, display the content of `SECRET_USERNAME` container environment variable.
  >   ```shell
  >   kubectl exec -i -t env-single-secret -- /bin/sh -c 'echo $SECRET_USERNAME'
  >   ```
  >   The output is similar to:
  >   ```
  >   backend-admin
  >   ```
  > [Distribute Credentials Securely Using Secrets > Define container environment variables using Secret data > Define container environment variables with data from multiple Secrets]
  > - As with the previous example, create the Secrets first.
  >   ```shell
  >   kubectl create secret generic backend-user --from-literal=backend-username='backend-admin'
  >   kubectl create secret generic db-user --from-literal=db-username='db-admin'
  >   ```
  > - Define the environment variables in the Pod specification.
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
  > - Create the Pod:
  >   ```shell
  >   kubectl create -f https://k8s.io/examples/pods/inject/pod-multiple-secret-env-variable.yaml
  >   ```
  > - In your shell, display the container environment variables.
  >   ```shell
  >   kubectl exec -i -t envvars-multiple-secrets -- /bin/sh -c 'env | grep _USERNAME'
  >   ```
  >   The output is similar to:
  >   ```
  >   DB_USERNAME=db-admin
  >   BACKEND_USERNAME=backend-admin
  >   ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `define-env-var`

**Question** (en, task): How do I set an environment variable for a container in a pod spec?

**Reference answer:** Add an `env` list to the container with `name` and `value` entries.

**Relevant documentation:**
- `tasks/inject-data-application/define-environment-variable-container.md`, section: *Define Environment Variables for a Container > Define an environment variable for a container*
  > [Define Environment Variables for a Container > Define an environment variable for a container]
  > When you create a Pod, you can set environment variables for the containers
  > that run in the Pod. To set environment variables, include the `env` or
  > `envFrom` field in the configuration file.
  > The `env` and `envFrom` fields have different effects.
  > `env`
  > : allows you to set environment variables for a container, specifying a value directly for each variable that you name.
  > `envFrom`
  > : allows you to set environment variables for a container by referencing either a ConfigMap or a Secret.
  >  When you use `envFrom`, all the key-value pairs in the referenced ConfigMap or Secret
  >  are set as environment variables for the container.
  >  You can also specify a common prefix string.
  > You can read more about ConfigMap
  > and Secret.
  > This page explains how to use `env`.
  > In this exercise, you create a Pod that runs one container. The configuration
  > file for the Pod defines an environment variable with name `DEMO_GREETING` and
  > value `"Hello from the environment"`. Here is the configuration manifest for the
  > Pod:
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
  >     image: gcr.io/google-samples/hello-app:2.0
  >     env:
  >     - name: DEMO_GREETING
  >       value: "Hello from the environment"
  >     - name: DEMO_FAREWELL
  >       value: "Such a sweet sorrow"
  > ```
  > 1. Create a Pod based on that manifest:
  >    ```shell
  >    kubectl apply -f https://k8s.io/examples/pods/inject/envars.yaml
  >    ```
  > 1. List the running Pods:
  >    ```shell
  >    kubectl get pods -l purpose=demonstrate-envars
  >    ```
  >    The output is similar to:
  >    ```
  >    NAME            READY     STATUS    RESTARTS   AGE
  >    envar-demo      1/1       Running   0          9s
  >    ```
  > 1. List the Pod's container environment variables:
  >    ```shell
  >    kubectl exec envar-demo -- printenv
  >    ```
  >    The output is similar to this:
  >    ```
  >    NODE_VERSION=4.4.2
  >    EXAMPLE_SERVICE_PORT_8080_TCP_ADDR=10.3.245.237
  >    HOSTNAME=envar-demo
  >    ...
  >    DEMO_GREETING=Hello from the environment
  >    DEMO_FAREWELL=Such a sweet sorrow
  >    ```
  >    ```
  >    NODE_VERSION=4.4.2
  >    EXAMPLE_SERVICE_PORT_8080_TCP_ADDR=10.3.245.237
  >    HOSTNAME=envar-demo
  >    ...
  >    DEMO_GREETING=Hello from the environment
  >    DEMO_FAREWELL=Such a sweet sorrow
  >    ```
  > The environment variables set using the `env` or `envFrom` field
  > override any environment variables specified in the container image.
  > Environment variables may reference each other, however ordering is important.
  > Variables making use of others defined in the same context must come later in
  > the list. Similarly, avoid circular references.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `hpa-create-cli`

**Question** (en, command): How do I create an autoscaler for a deployment from the command line?

**Reference answer:** `kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10`.

**Relevant documentation:**
- `tasks/run-application/horizontal-pod-autoscale-walkthrough.md`, section: *HorizontalPodAutoscaler Walkthrough > Create the HorizontalPodAutoscaler*
  > [HorizontalPodAutoscaler Walkthrough > Create the HorizontalPodAutoscaler {#create-horizontal-pod-autoscaler}]
  > Now that the server is running, create the autoscaler using `kubectl`. The
  > `kubectl autoscale` subcommand,
  > part of `kubectl`, helps you do this.
  > You will shortly run a command that creates a HorizontalPodAutoscaler that maintains
  > between 1 and 10 replicas of the Pods controlled by the php-apache Deployment that
  > you created in the first step of these instructions.
  > Roughly speaking, the HPA controller will increase and decrease
  > the number of replicas (by updating the Deployment) to maintain an average CPU utilization across all Pods of 50%.
  > The Deployment then updates the ReplicaSet - this is part of how all Deployments work in Kubernetes -
  > and then the ReplicaSet either adds or removes Pods based on the change to its `.spec`.
  > Since each pod requests 200 milli-cores by `kubectl run`, this means an average CPU usage of 100 milli-cores.
  > See Algorithm details for more details
  > on the algorithm.
  > Create the HorizontalPodAutoscaler:
  > ```shell
  > kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
  > ```
  > ```
  > horizontalpodautoscaler.autoscaling/php-apache autoscaled
  > ```
  > You can check the current status of the newly-made HorizontalPodAutoscaler, by running:
  > You can check the current status of the newly-made HorizontalPodAutoscaler, by running:
  > ```shell
  > # You can use "hpa" or "horizontalpodautoscaler"; either name works OK.
  > kubectl get hpa
  > ```
  > The output is similar to:
  > ```
  > NAME         REFERENCE                     TARGET    MINPODS   MAXPODS   REPLICAS   AGE
  > php-apache   Deployment/php-apache/scale   0% / 50%  1         10        1          18s
  > ```
  > (if you see other HorizontalPodAutoscalers with different names, that means they already existed,
  > and isn't usually a problem).
  > Please note that the current CPU consumption is 0% as there are no clients sending requests to the server
  > (the ``TARGET`` column shows the average across all the Pods controlled by the corresponding deployment).

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `lifecycle-hooks`

**Question** (en, task): How do I run a command right after a container starts, or just before it stops?

**Reference answer:** Define `lifecycle.postStart` and `lifecycle.preStop` handlers in the container spec.

**Relevant documentation:**
- `tasks/configure-pod-container/attach-handler-lifecycle-event.md`, section: *Attach Handlers to Container Lifecycle Events > Define postStart and preStop handlers*
  > [Attach Handlers to Container Lifecycle Events > Define postStart and preStop handlers]
  > In this exercise, you create a Pod that has one Container. The Container has handlers
  > for the postStart and preStop events.
  > Here is the configuration file for the Pod:
  > Example file `pods/lifecycle-events.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: lifecycle-demo
  > spec:
  >   containers:
  >   - name: lifecycle-demo-container
  >     image: nginx
  >     lifecycle:
  >       postStart:
  >         exec:
  >           command: ["/bin/sh", "-c", "echo Hello from the postStart handler > /usr/share/message"]
  >       preStop:
  >         exec:
  >           command: ["/bin/sh","-c","nginx -s quit; while killall -0 nginx; do sleep 1; done"]
  > ```
  > In the configuration file, you can see that the postStart command writes a `message`
  > file to the Container's `/usr/share` directory. The preStop command shuts down
  > nginx gracefully. This is helpful if the Container is being terminated because of a failure.
  > Create the Pod:
  >     kubectl apply -f https://k8s.io/examples/pods/lifecycle-events.yaml
  > Verify that the Container in the Pod is running:
  >     kubectl get pod lifecycle-demo
  > Get a shell into the Container running in your Pod:
  >     kubectl exec -it lifecycle-demo -- /bin/bash
  >     kubectl exec -it lifecycle-demo -- /bin/bash
  > In your shell, verify that the `postStart` handler created the `message` file:
  >     root@lifecycle-demo:/# cat /usr/share/message
  > The output shows the text written by the postStart handler:
  >     Hello from the postStart handler

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `default-memory-limit`

**Question** (en, task): How do I give every container in a namespace a default memory limit?

**Reference answer:** Create a LimitRange in the namespace with a `default` memory limit (and `defaultRequest`); containers without their own values get these defaults.

**Relevant documentation:**
- `tasks/administer-cluster/manage-resources/memory-default-namespace.md`, section: *Configure Default Memory Requests and Limits for a Namespace > Create a LimitRange and a Pod*
  > [Configure Default Memory Requests and Limits for a Namespace > Create a LimitRange and a Pod]
  > Here's a manifest for an example LimitRange.
  > The manifest specifies a default memory
  > request and a default memory limit.
  > Example file `admin/resource/memory-defaults.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: LimitRange
  > metadata:
  >   name: mem-limit-range
  > spec:
  >   limits:
  >   - default:
  >       memory: 512Mi
  >     defaultRequest:
  >       memory: 256Mi
  >     type: Container
  > ```
  > Create the LimitRange in the default-mem-example namespace:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/admin/resource/memory-defaults.yaml --namespace=default-mem-example
  > ```
  > Now if you create a Pod in the default-mem-example namespace, and any container
  > within that Pod does not specify its own values for memory request and memory limit,
  > then the control plane
  > applies default values: a memory request of 256MiB and a memory limit of 512MiB.
  > Here's an example manifest for a Pod that has one container. The container
  > does not specify a memory request and limit.
  > Example file `admin/resource/memory-defaults-pod.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: default-mem-demo
  > spec:
  >   containers:
  >   - name: default-mem-demo-ctr
  >     image: nginx
  > ```
  > Create the Pod.
  > Create the Pod.
  > ```shell
  > kubectl apply -f https://k8s.io/examples/admin/resource/memory-defaults-pod.yaml --namespace=default-mem-example
  > ```
  > View detailed information about the Pod:
  > ```shell
  > kubectl get pod default-mem-demo --output=yaml --namespace=default-mem-example
  > ```
  > The output shows that the Pod's container has a memory request of 256 MiB and
  > a memory limit of 512 MiB. These are the default values specified by the LimitRange.
  > ```shell
  > containers:
  > - image: nginx
  >   imagePullPolicy: Always
  >   name: default-mem-demo-ctr
  >   resources:
  >     limits:
  >       memory: 512Mi
  >     requests:
  >       memory: 256Mi
  > ```
  > Delete your Pod:
  > ```shell
  > kubectl delete pod default-mem-demo --namespace=default-mem-example
  > ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `namespace-quota`

**Question** (en, task): How do I cap the total CPU and memory all pods in a namespace can use?

**Reference answer:** Create a ResourceQuota with `requests.cpu`, `requests.memory`, `limits.cpu` and `limits.memory`; containers in the namespace then need requests and limits.

**Relevant documentation:**
- `tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace.md`, section: *Configure Memory and CPU Quotas for a Namespace > Create a ResourceQuota*
  > [Configure Memory and CPU Quotas for a Namespace > Create a ResourceQuota]
  > Here is a manifest for an example ResourceQuota:
  > Example file `admin/resource/quota-mem-cpu.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: ResourceQuota
  > metadata:
  >   name: mem-cpu-demo
  > spec:
  >   hard:
  >     requests.cpu: "1"
  >     requests.memory: 1Gi
  >     limits.cpu: "2"
  >     limits.memory: 2Gi
  > ```
  > Create the ResourceQuota:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/admin/resource/quota-mem-cpu.yaml --namespace=quota-mem-cpu-example
  > ```
  > View detailed information about the ResourceQuota:
  > ```shell
  > kubectl get resourcequota mem-cpu-demo --namespace=quota-mem-cpu-example --output=yaml
  > ```
  > The ResourceQuota places these requirements on the quota-mem-cpu-example namespace:
  > * For every Pod in the namespace, each container must have a memory request, memory limit, cpu request, and cpu limit.
  > * The memory request total for all Pods in that namespace must not exceed 1 GiB.
  > * The memory limit total for all Pods in that namespace must not exceed 2 GiB.
  > * The CPU request total for all Pods in that namespace must not exceed 1 cpu.
  > * The CPU limit total for all Pods in that namespace must not exceed 2 cpu.
  > See meaning of CPU
  > to learn what Kubernetes means by “1 CPU”.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `kustomize-overlays`

**Question** (en, task): How can I keep one base set of manifests and customize it per environment?

**Reference answer:** Use Kustomize: a base with the common resources and overlays per environment that reference the base; apply with `kubectl apply -k`.

**Relevant documentation:**
- `tasks/manage-kubernetes-objects/kustomization.md`, section: *Declarative Management of Kubernetes Objects Using Kustomize > Bases and Overlays*
  > [Declarative Management of Kubernetes Objects Using Kustomize > Bases and Overlays]
  > Kustomize has the concepts of **bases** and **overlays**. A **base** is a directory with a `kustomization.yaml`, which contains a
  > set of resources and associated customization. A base could be either a local directory or a directory from a remote repo,
  > as long as a `kustomization.yaml` is present inside. An **overlay** is a directory with a `kustomization.yaml` that refers to other
  > kustomization directories as its `bases`. A **base** has no knowledge of an overlay and can be used in multiple overlays.
  > The `kustomization.yaml` in an **overlay** directory may refer to multiple `bases`, combining all the resources defined
  > in these bases into a unified configuration. Additionally, it can apply customizations on top of these resources to meet specific
  > requirements.
  > Here is an example of a base:
  > Here is an example of a base:
  > ```shell
  > # Create a directory to hold the base
  > mkdir base
  > # Create a base/deployment.yaml
  > cat <<EOF > base/deployment.yaml
  > apiVersion: apps/v1
  > kind: Deployment
  > metadata:
  >   name: my-nginx
  > spec:
  >   selector:
  >     matchLabels:
  >       run: my-nginx
  >   replicas: 2
  >   template:
  >     metadata:
  >       labels:
  >         run: my-nginx
  >     spec:
  >       containers:
  >       - name: my-nginx
  >         image: nginx
  > EOF
  > # Create a base/service.yaml file
  > cat <<EOF > base/service.yaml
  > apiVersion: v1
  > kind: Service
  > metadata:
  >   name: my-nginx
  >   labels:
  >     run: my-nginx
  > spec:
  >   ports:
  >   - port: 80
  >     protocol: TCP
  >   selector:
  >     run: my-nginx
  > EOF
  > # Create a base/kustomization.yaml
  > cat <<EOF > base/kustomization.yaml
  > resources:
  > - deployment.yaml
  > - service.yaml
  > EOF
  > ```
  > This base can be used in multiple overlays. You can add different `namePrefix` or other cross-cutting fields
  > in different overlays. Here are two overlays using the same base.
  > ```shell
  > mkdir dev
  > cat <<EOF > dev/kustomization.yaml
  > resources:
  > - ../base
  > namePrefix: dev-
  > EOF
  > mkdir prod
  > cat <<EOF > prod/kustomization.yaml
  > resources:
  > - ../base
  > namePrefix: prod-
  > EOF
  > ```
- `tasks/manage-kubernetes-objects/kustomization.md`, section: *Declarative Management of Kubernetes Objects Using Kustomize > How to apply/view/delete objects using Kustomize*
  > [Declarative Management of Kubernetes Objects Using Kustomize > How to apply/view/delete objects using Kustomize]
  > Use `--kustomize` or `-k` in `kubectl` commands to recognize resources managed by `kustomization.yaml`.
  > Note that `-k` should point to a kustomization directory, such as
  > ```shell
  > kubectl apply -k <kustomization directory>/
  > ```
  > Given the following `kustomization.yaml`,
  > ```shell
  > # Create a deployment.yaml file
  > cat <<EOF > deployment.yaml
  > apiVersion: apps/v1
  > kind: Deployment
  > metadata:
  >   name: my-nginx
  > spec:
  >   selector:
  >     matchLabels:
  >       run: my-nginx
  >   replicas: 2
  >   template:
  >     metadata:
  >       labels:
  >         run: my-nginx
  >     spec:
  >       containers:
  >       - name: my-nginx
  >         image: nginx
  >         ports:
  >         - containerPort: 80
  > EOF
  > # Create a kustomization.yaml
  > cat <<EOF >./kustomization.yaml
  > namePrefix: dev-
  > labels:
  >   - pairs:
  >       app: my-nginx
  >     includeSelectors: true
  > resources:
  > - deployment.yaml
  > EOF
  > ```
  > Run the following command to apply the Deployment object `dev-my-nginx`:
  > ```shell
  > > kubectl apply -k ./
  > deployment.apps/dev-my-nginx created
  > ```
  > Run one of the following commands to view the Deployment object `dev-my-nginx`:
  > ```shell
  > kubectl get -k ./
  > ```
  > ```shell
  > kubectl describe -k ./
  > ```
  > ```shell
  > kubectl describe -k ./
  > ```
  > Run the following command to compare the Deployment object `dev-my-nginx` against the state
  > that the cluster would be in if the manifest was applied:
  > ```shell
  > kubectl diff -k ./
  > ```
  > Run the following command to delete the Deployment object `dev-my-nginx`:
  > ```shell
  > > kubectl delete -k ./
  > deployment.apps "dev-my-nginx" deleted
  > ```

*Drafting note:* golden v2 draft (2026-11-07) | self-check: aligned with the referenced text

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---
