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
  > If there are two possible nodes that match the
  > `preferredDuringSchedulingIgnoredDuringExecution` rule, one with the
  > `label-1:key-1` label and another with the `label-2:key-2` label, the scheduler
  > considers the `weight` of each node and adds the weight to the other scores for
  > that node, and schedules the Pod onto the node with the highest final score.
  > If you want Kubernetes to successfully schedule the Pods in this example, you
  > must have existing nodes with the `kubernetes.io/os=linux` label.
  > [Assigning Pods to Nodes > Affinity and anti-affinity > Node affinity > Node affinity per scheduling profile]
  > When configuring multiple scheduling profiles, you can associate
  > a profile with a node affinity, which is useful if a profile only applies to a specific set of nodes.
  > To do so, add an `addedAffinity` to the `args` field of the `NodeAffinity` plugin
  > in the scheduler configuration. For example:
  > ```yaml
  > apiVersion: kubescheduler.config.k8s.io/v1
  > kind: KubeSchedulerConfiguration
  > profiles:
  >   - schedulerName: default-scheduler
  >   - schedulerName: foo-scheduler
  >     pluginConfig:
  >       - name: NodeAffinity
  >         args:
  >           addedAffinity:
  >             requiredDuringSchedulingIgnoredDuringExecution:
  >               nodeSelectorTerms:
  >               - matchExpressions:
  >                 - key: scheduler-profile
  >                   operator: In
  >                   values:
  >                   - foo
  > ```
  > The `addedAffinity` is applied to all Pods that set `.spec.schedulerName` to `foo-scheduler`, in addition to the
  > NodeAffinity specified in the PodSpec.
  > That is, in order to match the Pod, nodes need to satisfy `addedAffinity` and
  > the Pod's `.spec.NodeAffinity`.
  > Since the `addedAffinity` is not visible to end users, its behavior might be
  > unexpected to them. Use node labels that have a clear correlation to the
  > scheduler profile name.
  > The DaemonSet controller, which creates Pods for DaemonSets,
  > does not support scheduling … (section continues)

*Drafting note:* human review (Youssef Zemzem, 2026-11-07): added the node-labels section; no kubectl command claimed | human review 2 (Youssef Zemzem, 2026-11-07): required vs preferred affinity made explicit

**Decision** (tick one):
- [ ] ✅ Correct as written
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
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---
