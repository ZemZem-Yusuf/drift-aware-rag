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

### `fr-memory-limit-exceeded`

**Question** (fr, troubleshooting): Que se passe-t-il si un conteneur dépasse sa limite de mémoire ?

**Reference answer:** Il peut être arrêté (OOMKilled), puis redémarré par le kubelet si le conteneur peut être redémarré.

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

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 5 (Youssef Zemzem, 2026-11-07): wording aligned with the docs ('si le conteneur peut être redémarré')

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-node-status`

**Question** (fr, troubleshooting): Comment voir l'état et les conditions d'un nœud ?

**Reference answer:** `kubectl describe node <nom>` ; l'état du nœud comprend notamment ses conditions.

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

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 5 (Youssef Zemzem, 2026-11-07): removed the condition examples the French section doesn't list

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---
